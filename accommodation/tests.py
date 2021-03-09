import unittest

from django.test          import TestCase, Client
from django.test.utils    import override_settings

from user.models          import User, SocialPlatform
from review.models        import Review
from accommodation.models import Category, Accommodation, Image

maxDiff = None

class AccommodationDetailTest(TestCase):
    def setUp(self):
        SocialPlatform.objects.create(id=1, name='kakao')
        
        User.objects.create(
            id                 = 1,
            email              = 'test@gmail.com',
            name               = 'test',
            profile_image      = 'profile_image.jpg',
            social_platform_id = 1
        )
        User.objects.create(
            id                 = 2,
            email              = 'test2@gmail.com',
            name               = 'test2',
            profile_image      = 'profile_image2.jpg',
            social_platform_id = 1
        )

        Category.objects.create(
            id          = 1,
            name        = '집 전체', 
            description = '집 전체를 사용하게 됩니다.'
        )

        Accommodation.objects.create(
            id                 = 1,
            category_id        = 1,
            user_id            = 1,
            title              = 'test house', 
            address            = '서울특별시 강남구 테헤란로',
            latitude           = 37.5,
            longitude          = 127.05,
            description        = 'description',
            max_capacity       = 5,
            price              = 10000,
            cleaning_fee       = 1000,
            number_of_bed      = 1,
            number_of_bedroom  = 1,
            number_of_bathroom = 1
        )

        Image.objects.create(
            accommodation_id = 1,
            image_url        = 'house_image.jpg'
        )

        Image.objects.create(
            accommodation_id = 1,
            image_url        = 'house_image2.jpg'
        )

        Review.objects.create(
            id                 = 1,
            accommodation_id   = 1, 
            user_id            = 1, 
            clean_rate         = 5,
            communication_rate = 5,
            checkin_rate       = 5,
            accuracy_rate      = 5,
            location_rate      = 5,
            value_rate         = 5,
            content            = 'good'
        )

    def tearDown(self):
        SocialPlatform.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()
        Accommodation.objects.all().delete()
        Image.objects.all().delete()
        Review.objects.all().delete()

    @override_settings(DEBUG=True)
    def test_accommodation_detail_get_success(self):
        client   = Client()
        response = client.get('/accommodation/1')
        print(response)
        self.assertEqual(response.json(),
            {
               "id":1,
               "title":"test house",
               "address":"서울특별시 강남구 테헤란로",
               "lat":"37.500000",
               "long":"127.050000",
               "firstImg":"house_image.jpg",
               "img":[
                  "house_image2.jpg"
               ],
               "description":"description",
               "onedayPrice":"10000.00",
               "cleaningFee":"1000.00",
               "hostName":"test",
               "hostProfile":"profile_image.jpg",
               "roomType":{
                  "name":"집 전체",
                  "description":"집 전체를 사용하게 됩니다."
               },
               "maxPeople":5,
               "beds":1,
               "bedrooms":1,
               "bathrooms":1,
               "totalCount":1,
               "totalAvg":"5.00",
               "grade":[
                  {
                     "average":"5.0",
                     "gradeValue":100
                  },
                  {
                     "average":"5.0",
                     "gradeValue":100
                  },
                  {
                     "average":"5.0",
                     "gradeValue":100
                  },
                  {
                     "average":"5.0",
                     "gradeValue":100
                  },
                  {
                     "average":"5.0",
                     "gradeValue":100
                  },
                  {
                     "average":"5.0",
                     "gradeValue":100
                  }
               ],
               "comment":[
                  {
                     "reviewid"   : 1,
                     "userName"   : "test",
                     "userProfile": "profile_image.jpg",
                     "content"    : "good",
                     "createdAt"  : "202103"
                  }
               ]
            }
        )
        self.assertEqual(response.status_code, 200)  

    def test_accommodation_detail_get_not_found(self):
        client   = Client()
        response = client.get('/accommodation/99999999')
        self.assertEqual(response.json(),
            {
                "message": "PAGE_NOT_FOUND"
            }
        )
        self.assertEqual(response.status_code, 404)  

