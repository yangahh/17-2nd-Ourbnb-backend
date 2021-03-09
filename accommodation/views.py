import json
from statistics import mean

from django.http                import JsonResponse
from django.views               import View
from django.db.models           import Avg
from django.utils.dateformat    import DateFormat
from django.db.models.functions import Coalesce

from .models                    import Accommodation

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
            'totalCount': accommodation.review_set.count(),
            'totalAvg'  : round(mean(review_avg.values()), 2),
            'grade'     : [{
                'average'   : round(each_average, 1),
                'gradeValue': round(each_average * 100 / 5)
            } for each_average in review_avg.values()],
            'comment'  : [{
                'reviewid'   : review.id,
                'userName'   : review.user.name,
                'userProfile': review.user.profile_image,
                'content'    : review.content,
                'createdAt'  : DateFormat(review.created_at).format('Ym')
            } for review in accommodation.review_set.all()]
        }

        return JsonResponse(data, status=200)
