import json
import math
import boto3
import uuid 

from statistics                 import mean
from datetime                   import datetime
from json.decoder               import JSONDecodeError

from django.http                import JsonResponse
from django.views               import View
from django.db                  import connection
from django.db.models           import Avg, Q
from django.utils.dateformat    import DateFormat
from django.db.models.functions import Coalesce
from django.core.exceptions     import ObjectDoesNotExist

from user.utils                 import login_decorator
from .models                    import Accommodation, Category, Image, UnavailableDate
from my_settings                import (
                                    AWS_S3_ACCESS_KEY_ID, 
                                    AWS_S3_SECRET_ACCESS_KEY, 
                                    AWS_S3_STORAGE_BUCKET_NAME,
                                )  


class AccommodationListView(View):
    def get(self, request):         
        checkin    = request.GET.get('checkin')
        checkout   = request.GET.get('checkout')
        guests     = request.GET.get('guests')
        categories = request.GET.getlist('roomtype') 
        price_min  = request.GET.get('min')
        price_max  = request.GET.get('max')
        limit      = int(request.GET.get('limit', '15'))
        offset     = int(request.GET.get('offset', '15'))

        condition = Q()
        if (checkin and checkout):
            condition.add((
                ( 
                    Q(unavailabledate__end_date__lte= datetime.strptime(checkin, "%Y-%m-%d").date()) 
                )|(
                    Q(unavailabledate__start_date__gte= datetime.strptime(checkout, "%Y-%m-%d").date())                    
                )
            ), Q.OR)

        if guests:
            condition.add(Q(max_capacity__gt=guests), Q.AND)

        if len(categories):
            category_dict = {
                'entire'  : '집 전체',
                'private' : '개인실',
                'shared'  : '다인실',
                'hotel'   : '호텔 객실'
            }
            categories = [category_dict[category] for category in categories]

            condition.add(Q(category__name__in=categories), Q.AND)

        if price_min:
            condition.add(Q(price__gt=price_min), Q.AND)
        if price_max:
            condition.add(Q(price__lt=price_max), Q.AND)
        
        accommodations = Accommodation.objects.prefetch_related('image_set', 'review_set').select_related('category').filter(condition).distinct()
        
        index = math.ceil(len(accommodations)/limit)
        accommodations = accommodations[offset-limit:offset]

        data = [
            {
            'id'       : accommodation.id,
            'img'      : [image.image_url for image in accommodation.image_set.all()],
            'location' : accommodation.address.split(' ')[1] + ' ' + accommodation.category.name,
            'title'    : accommodation.title,
            'MaxNum'   : accommodation.max_capacity,
            'grade'    : str(round(mean(accommodation.review_set.all().aggregate(
                Avg('clean_rate'),
                Avg('communication_rate'),
                Avg('checkin_rate'),
                Avg('accuracy_rate'),
                Avg('location_rate'),
                Avg('value_rate')).values()), 2)) 
                if accommodation.review_set.exists() else '0',
            'gradeNum' : accommodation.review_set.count(),
            'price'    : round(accommodation.price, 0),
            'lat'      : accommodation.latitude,
            'long'     : accommodation.longitude,
            'bed'      : accommodation.number_of_bed,
            'bedroom'  : accommodation.number_of_bedroom,
            'bathroom' : accommodation.number_of_bathroom
            }
        for accommodation in accommodations]

        return JsonResponse({'message': 'SUCCESS', 'data': data, 'index': index}, status=200)

    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            new_accommodation = Accommodation.objects.create(
                category           = Category.objects.get(name=data['roomType']),
                user               = request.user,
                title              = data['title'],
                address            = data['address'],
                latitude           = data['lat'],
                longitude          = data['long'],
                description        = data['description'],
                max_capacity       = data['maxPeople'],
                price              = data['onedayPrice'],
                cleaning_fee       = data['cleaningFee'],
                number_of_bed      = data['beds'],
                number_of_bedroom  = data['bedrooms'],
                number_of_bathroom = data['bathrooms']
            )

            image_url_list = data['imgUrls']
            for image_url in image_url_list:
                Image.objects.create(
                    accommodation = new_accommodation,
                    image_url     = image_url
                )

            unavailable_dates_list = data['unavailableDates']
            for unavailable_date in unavailable_dates_list:
                start_date = datetime.strptime(unavailable_date['start_date'], '%Y-%m-%d').date()
                end_date   = datetime.strptime(unavailable_date['end_date'], '%Y-%m-%d').date()

                UnavailableDate.objects.create(
                    accommodation = new_accommodation,
                    start_date    = start_date,
                    end_date      = end_date
                )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({'message': 'CATEGORY_DOES_NOT_EXIST'}, status=400)

class FileUploadView(View):
    def post(self, request):
        AWS_S3_CREDS = {
            "aws_access_key_id"    : AWS_S3_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_S3_SECRET_ACCESS_KEY
        }
        s3_client = boto3.client('s3', **AWS_S3_CREDS)

        files = request.FILES.getlist('fileNames')

        if not files:
            return JsonResponse({'message': 'IMAGE_DOES_NOT_EXIST'}, status=400)

        file_urls = []
        for file in files:
            file_type = file.content_type.split('/')[-1]
            file_name = str(uuid.uuid4()).replace('-','') + DateFormat(datetime.now()).format('Ymd')+ '.' + file_type

            s3_client.upload_fileobj(
                file,
                AWS_S3_STORAGE_BUCKET_NAME,
                file_name,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
            file_urls.append(f"https://{AWS_S3_STORAGE_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{file_name}")

        return JsonResponse({'file_urls': file_urls}, status=200)

class AccomodationDetailView(View):
    def get(self, request, accommodation_id):
        if not Accommodation.objects.filter(id=accommodation_id).exists():
            return JsonResponse({"message": "PAGE_NOT_FOUND"}, status=404)

        accommodation = Accommodation.objects.select_related('user', 'category').prefetch_related('review_set').get(id=accommodation_id)
        review_avg    = accommodation.review_set.aggregate(
                            clean_avg         = Coalesce(Avg('clean_rate'), 0),
                            accuracy_avg      = Coalesce(Avg('accuracy_rate'), 0),
                            communication_avg = Coalesce(Avg('communication_rate'), 0),
                            location_avg      = Coalesce(Avg('location_rate'), 0),
                            checkin_avg       = Coalesce(Avg('checkin_rate'), 0),
                            value_avg         = Coalesce(Avg('value_rate'), 0),
                        )
        
        data = {
            'id'         : accommodation.id,
            'title'      : accommodation.title,
            'address'    : accommodation.address,
            'lat'        : accommodation.latitude,
            'long'       : accommodation.longitude,
            'firstImg'   : accommodation.image_set.first().image_url,
            'img'        : [image.image_url for image in accommodation.image_set.all()[1:]],
            'description': accommodation.description,
            'onedayPrice': accommodation.price,
            'cleaningFee': accommodation.cleaning_fee,
            'hostName'   : accommodation.user.name,
            'hostProfile': accommodation.user.profile_image,
            'roomType'   : {
                'name'       : accommodation.category.name,
                'description': accommodation.category.description
            },
            'maxPeople'  : accommodation.max_capacity,
            'beds'       : accommodation.number_of_bed, 
            'bedrooms'   : accommodation.number_of_bedroom, 
            'bathrooms'  : accommodation.number_of_bathroom,
            'totalCount' : accommodation.review_set.count(),
            'totalAvg'   : round(mean(review_avg.values()), 2),
            'grade'      : [{
                'average'   : round(each_average, 1),
                'gradeValue': round(each_average * 100 / 5)
            } for each_average in review_avg.values()],
            'comment'    : [{
                'reviewid'   : review.id,
                'userName'   : review.user.name,
                'userProfile': review.user.profile_image,
                'content'    : review.content,
                'createdAt'  : DateFormat(review.created_at).format('Ym')
            } for review in accommodation.review_set.all()]
        }

        return JsonResponse(data, status=200)


