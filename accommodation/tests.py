import unittest
import json
import jwt
from datetime import datetime
from decimal  import Decimal

from django.test          import TestCase, Client
from django.test.utils    import override_settings

from user.models          import User, SocialPlatform
from review.models        import Review
from accommodation.models import Category, Accommodation, Image, UnavailableDate
from my_settings          import SECRET_KEY, ALGORITHM

maxDiff = None
client  = Client()

class AccommodationRegisterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SocialPlatform.objects.create(id=1, name='kakao')
        
        User.objects.create(
            id                 = 1,
            email              = 'test@gmail.com',
            name               = 'test',
            profile_image      = 'profile_image.jpg',
            social_platform_id = 1
        )

        Category.objects.create(
            id          = 1,
            name        = '집 전체', 
            description = '집 전체를 사용하게 됩니다.'
        )

    def test_accommodation_register_post_success(self):
        user         = User.objects.get(id=1)
        access_token = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM)
        headers      = {'HTTP_Authorization': access_token}
        body = {
            'roomType'    : '집 전체',
            'title'       : 'nice house',
            'address'     : '선릉',
            'lat'         : 37.5,
            'long'        : 127.05,
            'description' : 'desc',
            'maxPeople'   : 5,
            'onedayPrice' : 120000.00,
            'cleaningFee' : 1000.050000,
            'beds'        : 1,
            'bedrooms'    : 2,
            'bathrooms'   : 1,
            'imgUrls'     : ['http://image1.jpg', 'http://image2.jpg'],
            'unavailableDates': [
                {'start_date': '2021-03-04', 'end_date': '2021-03-09'}, 
                {'start_date': '2021-03-10', 'end_date': '2021-03-17'}, 
            ]
        }
        response = client.post('/accommodation', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message': 'SUCCESS'
            }
        )

    def test_accommodation_register_post_key_fail(self):
        user         = User.objects.get(id=1)
        access_token = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM)
        headers      = {'HTTP_Authorization': access_token}
        body = {
            'roomType'    : '집 전체',
            'title'       : 'nice house',
            'address'     : '선릉',
            'lat'         : 37.5,
            'long'        : 127.05,
            'description' : 'desc',
            'maxPeople'   : 5,
            'onedayPrice' : 120000.00,
            'cleaningFee' : 1000.050000,
            'beds'        : 1,
            'bedrooms'    : 2,
            'bathrooms'   : 1,
            'imgUrls'     : ['http://image1.jpg', 'http://image2.jpg']
        }
        response = client.post('/accommodation', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message': 'KEY_ERROR'
            }
        )

    def test_accommodation_register_fail_non_category(self):
        user         = User.objects.get(id=1)
        access_token = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM)
        headers      = {'HTTP_Authorization': access_token}
        body = {
            'roomType'    : '전체',
            'title'       : 'nice house',
            'address'     : '선릉',
            'lat'         : 37.5,
            'long'        : 127.05,
            'description' : 'desc',
            'maxPeople'   : 5,
            'onedayPrice' : 120000.00,
            'cleaningFee' : 1000.050000,
            'beds'        : 1,
            'bedrooms'    : 2,
            'bathrooms'   : 1,
            'imgUrls'     : ['http://image1.jpg', 'http://image2.jpg'],
            'unavailableDates': [
                {'start_date': '2021-03-04', 'end_date': '2021-03-09'}, 
                {'start_date': '2021-03-10', 'end_date': '2021-03-17'}, 
            ]
        }
        response = client.post('/accommodation', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'CATEGORY_DOES_NOT_EXIST'
            }
        )

    def test_accommodation_register_invalid_token(self):
        user         = User.objects.get(id=1)
        access_token = jwt.encode({'user': user.id}, 'secret', ALGORITHM)
        headers      = {'HTTP_Authorization': access_token}
        body = {
            'roomType'    : '집 전체',
            'title'       : 'nice house',
            'address'     : '선릉',
            'lat'         : 37.5,
            'long'        : 127.05,
            'description' : 'desc',
            'maxPeople'   : 5,
            'onedayPrice' : 120000.00,
            'cleaningFee' : 1000.050000,
            'beds'        : 1,
            'bedrooms'    : 2,
            'bathrooms'   : 1,
            'imgUrls'     : ['http://image1.jpg', 'http://image2.jpg'],
            'unavailableDates': [
                {'start_date': '2021-03-04', 'end_date': '2021-03-09'}, 
                {'start_date': '2021-03-10', 'end_date': '2021-03-17'}, 
            ]
        }
        response = client.post('/accommodation', json.dumps(body), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_TOKEN'
            }
        )

class AccommodationDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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

    @override_settings(DEBUG=True)
    def test_accommodation_detail_get_success(self):
        response = client.get('/accommodation/1')
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
        response = client.get('/accommodation/99999999')
        self.assertEqual(response.json(),
            {
                "message": "PAGE_NOT_FOUND"
            }
        )
        self.assertEqual(response.status_code, 404)  

class AccommodationListTest(TestCase):
    @classmethod
    def setUpTestData(cls): 
        SocialPlatform.objects.create(id=1, name='kakao')

        User.objects.create(
            id                 = 1,
            email              = 'test@gmail.com',
            name               = 'test',
            profile_image      = 'profile_image.jpg',
            social_platform_id = 1
        )

        Category.objects.create(
            id          = 1,
            name        = '집 전체',
            description = '집 전체쟈나'
        )

        Category.objects.create(
            id          = 2,
            name        = '개인실',
            description = '개인실이쟈나'
        )

        Accommodation.objects.create(
            id                 = 1, 
            category           = Category.objects.get(id=1),
            user               = User.objects.get(id=1),
            title              = 'test accommodation 1',
            address            = '서울특별시 강남구 테헤란로',
            latitude           = 37.5111,
            longitude          = 101.2222,
            description        = 'test description',
            max_capacity       = 5,
            price              = 16000.00,
            cleaning_fee       = 3000.00,
            number_of_bed      = 1,
            number_of_bedroom  = 2,
            number_of_bathroom = 1
        )

        UnavailableDate.objects.create(
            id            = 1,
            accommodation = Accommodation.objects.get(id=1),
            start_date    = datetime.strptime('2021-03-17', "%Y-%m-%d").date(),
            end_date      = datetime.strptime('2021-03-18', "%Y-%m-%d").date(),
        )

        Image.objects.create(
            id            = 1,
            accommodation = Accommodation.objects.get(id=1),
            image_url     = 'test_accommodation_1_image_1.jpg'
        )

        Image.objects.create(
            id            = 2,
            accommodation = Accommodation.objects.get(id=1),
            image_url     = 'test_accommodation_1_image_2.jpg'
        )

        Review.objects.create(
            id                 = 1,
            accommodation      = Accommodation.objects.get(title='test accommodation 1'),
            user               = User.objects.get(email='test@gmail.com'),
            clean_rate         = 5,
            communication_rate = 5,
            checkin_rate       = 5,
            accuracy_rate      = 5,
            location_rate      = 5,
            value_rate         = 5,
            content            = 'good'
        )

        Accommodation.objects.create(
            id                 = 2, 
            category           = Category.objects.get(id=1),
            user               = User.objects.get(id=1),
            title              = 'test accommodation 2',
            address            = '서울특별시 강남구 테헤란로',
            latitude           = 37.4444,
            longitude          = 100.1111,
            description        = 'test description',
            max_capacity       = 3,
            price              = 20000.00,
            cleaning_fee       = 2500.00,
            number_of_bed      = 1,
            number_of_bedroom  = 1,
            number_of_bathroom = 2
        )

        UnavailableDate.objects.create(
            id            = 2,
            accommodation = Accommodation.objects.get(id=2),
            start_date    = datetime.strptime('2021-03-20', "%Y-%m-%d").date(),
            end_date      = datetime.strptime('2021-03-22', "%Y-%m-%d").date(),
        )

        Image.objects.create(
            id            = 3,
            accommodation = Accommodation.objects.get(id=2),
            image_url     = 'test_accommodation_2_image_1.jpg'
        )

        Image.objects.create(
            id            = 4,
            accommodation = Accommodation.objects.get(id=2),
            image_url     = 'test_accommodation_2_image_2.jpg'
        )

        Accommodation.objects.create(
            id                 = 3, 
            category           = Category.objects.get(id=2),
            user               = User.objects.get(id=1),
            title              = 'test accommodation 3',
            address            = '서울특별시 강남구 테헤란로',
            latitude           = 37.3333,
            longitude          = 100.3333,
            description        = 'test description',
            max_capacity       = 2,
            price              = 30000.00,
            cleaning_fee       = 3500.00,
            number_of_bed      = 1,
            number_of_bedroom  = 3,
            number_of_bathroom = 1
        )

        UnavailableDate.objects.create(
            id            = 3,
            accommodation = Accommodation.objects.get(id=3),
            start_date    = datetime.strptime('2021-03-29', "%Y-%m-%d").date(),
            end_date      = datetime.strptime('2021-04-01', "%Y-%m-%d").date(),
        )

        Image.objects.create(
            id            = 5,
            accommodation = Accommodation.objects.get(id=3),
            image_url     = 'test_accommodation_3_image_1.jpg'
        )

        Image.objects.create(
            id            = 6,
            accommodation = Accommodation.objects.get(id=3),
            image_url     = 'test_accommodation_3_image_2.jpg'
        )
      
    def test_get_accommodation_list_view_success_checkin_03_17_checkout_03_23(self):
        response = client.get('/accommodation?checkin=2021-03-17&checkout=2021-03-23&guests=1')
        self.assertEqual(response.json()["data"],
        [{
            'id'       : 3,
            'img'      : ['test_accommodation_3_image_1.jpg', 'test_accommodation_3_image_2.jpg'],
            'location' : '강남구 개인실',
            'title'    : 'test accommodation 3',
            'MaxNum'   : 2,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '30000',
            'lat'      : '37.333300',
            'long'     : '100.333300',
            'bed'      : 1,
            'bedroom'  : 3,
            'bathroom' : 1
         }])

        self.assertEqual(response.status_code, 200)  
    
    def test_get_accommodation_list_view_success_checkin_03_15_checkout_03_18(self):
        response = client.get('/accommodation?checkin=2021-03-15&checkout=2021-03-18&guests=1')
        self.assertEqual(response.json()["data"],
        [{
            'id'       : 2,
            'img'      : ['test_accommodation_2_image_1.jpg', 'test_accommodation_2_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 2',
            'MaxNum'   : 3,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '20000',
            'lat'      : '37.444400',
            'long'     : '100.111100',
            'bed'      : 1,
            'bedroom'  : 1,
            'bathroom' : 2
         }, 
         {
            'id'       : 3,
            'img'      : ['test_accommodation_3_image_1.jpg', 'test_accommodation_3_image_2.jpg'],
            'location' : '강남구 개인실',
            'title'    : 'test accommodation 3',
            'MaxNum'   : 2,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '30000',
            'lat'      : '37.333300',
            'long'     : '100.333300',
            'bed'      : 1,
            'bedroom'  : 3,
            'bathroom' : 1
         }])

        self.assertEqual(response.status_code, 200) 

    def test_get_accommodation_list_view_success_checkin_03_28_checkout_04_02(self):
        response = client.get('/accommodation?checkin=2021-03-28&checkout=2021-04-02&guests=1')
        self.assertEqual(response.json()["data"],
        [{
            'id'       : 1,
            'img'      : ['test_accommodation_1_image_1.jpg', 'test_accommodation_1_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 1',
            'MaxNum'   : 5,
            'grade'    : '5.00',
            'gradeNum' : 1,
            'price'    : '16000',
            'lat'      : '37.511100',
            'long'     : '101.222200',
            'bed'      : 1,
            'bedroom'  : 2,
            'bathroom' : 1
         }, 
         {
            'id'       : 2,
            'img'      : ['test_accommodation_2_image_1.jpg', 'test_accommodation_2_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 2',
            'MaxNum'   : 3,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '20000',
            'lat'      : '37.444400',
            'long'     : '100.111100',
            'bed'      : 1,
            'bedroom'  : 1,
            'bathroom' : 2
         }])     

    def test_get_accommodation_list_view_success_checkin_03_20_checkout_04_01(self):
        response = client.get('/accommodation?checkin=2021-03-20&checkout=2021-04-01&guests=1')
        self.assertEqual(response.json()["data"],
        [{
            'id'       : 1,
            'img'      : ['test_accommodation_1_image_1.jpg', 'test_accommodation_1_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 1',
            'MaxNum'   : 5,
            'grade'    : '5.00',
            'gradeNum' : 1,
            'price'    : '16000',
            'lat'      : '37.511100',
            'long'     : '101.222200',
            'bed'      : 1,
            'bedroom'  : 2,
            'bathroom' : 1
         }])

        self.assertEqual(response.status_code, 200)  

    def test_get_accommodation_list_view_success_checkin_04_12_checkout_04_30(self):
        response = client.get('/accommodation?checkin=2021-04-12&checkout=2021-04-30&guests=1')
        self.assertEqual(response.json()["data"],
        [{
            'id'       : 1,
            'img'      : ['test_accommodation_1_image_1.jpg', 'test_accommodation_1_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 1',
            'MaxNum'   : 5,
            'grade'    : '5.00',
            'gradeNum' : 1,
            'price'    : '16000',
            'lat'      : '37.511100',
            'long'     : '101.222200',
            'bed'      : 1,
            'bedroom'  : 2,
            'bathroom' : 1
         }, 
         {
            'id'       : 2,
            'img'      : ['test_accommodation_2_image_1.jpg', 'test_accommodation_2_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 2',
            'MaxNum'   : 3,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '20000',
            'lat'      : '37.444400',
            'long'     : '100.111100',
            'bed'      : 1,
            'bedroom'  : 1,
            'bathroom' : 2
         },
         {
            'id'       : 3,
            'img'      : ['test_accommodation_3_image_1.jpg', 'test_accommodation_3_image_2.jpg'],
            'location' : '강남구 개인실',
            'title'    : 'test accommodation 3',
            'MaxNum'   : 2,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '30000',
            'lat'      : '37.333300',
            'long'     : '100.333300',
            'bed'      : 1,
            'bedroom'  : 3,
            'bathroom' : 1
         }])

        self.assertEqual(response.status_code, 200)  

    def test_get_accommodation_list_view_success_checkin_03_12_checkout_04_30(self):
        response = client.get('/accommodation?checkin=2021-03-12&checkout=2021-04-30&guests=1')
        self.assertEqual(response.json()["data"],[])
        self.assertEqual(response.status_code, 200)  
    
    def test_get_accommodation_list_view_success_room_entire_private(self):
        response = client.get('/accommodation?checkin=2021-04-17&checkout=2021-04-20&guests=1&roomtype=entire&roomtype=private')
        self.assertEqual(response.json()["data"],
        [{
            'id'       : 1,
            'img'      : ['test_accommodation_1_image_1.jpg', 'test_accommodation_1_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 1',
            'MaxNum'   : 5,
            'grade'    : '5.00',
            'gradeNum' : 1,
            'price'    : '16000',
            'lat'      : '37.511100',
            'long'     : '101.222200',
            'bed'      : 1,
            'bedroom'  : 2,
            'bathroom' : 1
         }, 
         {
            'id'       : 2,
            'img'      : ['test_accommodation_2_image_1.jpg', 'test_accommodation_2_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 2',
            'MaxNum'   : 3,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '20000',
            'lat'      : '37.444400',
            'long'     : '100.111100',
            'bed'      : 1,
            'bedroom'  : 1,
            'bathroom' : 2
         },
         {
            'id'       : 3,
            'img'      : ['test_accommodation_3_image_1.jpg', 'test_accommodation_3_image_2.jpg'],
            'location' : '강남구 개인실',
            'title'    : 'test accommodation 3',
            'MaxNum'   : 2,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '30000',
            'lat'      : '37.333300',
            'long'     : '100.333300',
            'bed'      : 1,
            'bedroom'  : 3,
            'bathroom' : 1
         }   
        ])
        self.assertEqual(response.status_code, 200)  

    def test_get_accommodation_list_view_success_room_entire(self):
        response = client.get('/accommodation?checkin=2021-04-17&checkout=2021-04-20&guests=1&roomtype=entire')
        self.assertEqual(response.json()["data"],
        [{    
            'id'       : 1,
            'img'      : ['test_accommodation_1_image_1.jpg', 'test_accommodation_1_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 1',
            'MaxNum'   : 5,
            'grade'    : '5.00',
            'gradeNum' : 1,
            'price'    : '16000',
            'lat'      : '37.511100',
            'long'     : '101.222200',
            'bed'      : 1,
            'bedroom'  : 2,
            'bathroom' : 1
         }, 
         {
            'id'       : 2,
            'img'      : ['test_accommodation_2_image_1.jpg', 'test_accommodation_2_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 2',
            'MaxNum'   : 3,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '20000',
            'lat'      : '37.444400',
            'long'     : '100.111100',
            'bed'      : 1,
            'bedroom'  : 1,
            'bathroom' : 2
         }
        ])
        self.assertEqual(response.status_code, 200) 

    def test_get_accommodation_list_view_success_room_private(self):
        response = client.get('/accommodation?checkin=2021-04-17&checkout=2021-04-20&guests=1&roomtype=private')
        self.assertEqual(response.json()["data"],
        [{
            'id'       : 3,
            'img'      : ['test_accommodation_3_image_1.jpg', 'test_accommodation_3_image_2.jpg'],
            'location' : '강남구 개인실',
            'title'    : 'test accommodation 3',
            'MaxNum'   : 2,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '30000',
            'lat'      : '37.333300',
            'long'     : '100.333300',
            'bed'      : 1,
            'bedroom'  : 3,
            'bathroom' : 1
         }
        ])
        self.assertEqual(response.status_code, 200)  
        
    def test_get_accommodation_list_view_success_room_hotel(self):
        response = client.get('/accommodation?checkin=2021-04-17&checkout=2021-04-20&guests=1&roomtype=hotel')
        self.assertEqual(response.json()["data"],[])
        self.assertEqual(response.status_code, 200)  
    
    def test_get_accommodation_list_view_success_min_10000(self):
        response = client.get('/accommodation?checkin=2021-04-17&checkout=2021-04-20&guests=1&roomtype=entire&min=19000')
        self.assertEqual(response.json()["data"],
        [
            {
            'id'       : 2,
            'img'      : ['test_accommodation_2_image_1.jpg', 'test_accommodation_2_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 2',
            'MaxNum'   : 3,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '20000',
            'lat'      : '37.444400',
            'long'     : '100.111100',
            'bed'      : 1,
            'bedroom'  : 1,
            'bathroom' : 2
         }
        ])
        self.assertEqual(response.status_code, 200) 
    
    def test_get_accommodation_list_view_success_max_40000(self):
        response = client.get('/accommodation?checkin=2021-04-17&checkout=2021-04-20&guests=1&max=40000')
        self.assertEqual(response.json()["data"],
        [{
            'id'       : 1,
            'img'      : ['test_accommodation_1_image_1.jpg', 'test_accommodation_1_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 1',
            'MaxNum'   : 5,
            'grade'    : '5.00',
            'gradeNum' : 1,
            'price'    : '16000',
            'lat'      : '37.511100',
            'long'     : '101.222200',
            'bed'      : 1,
            'bedroom'  : 2,
            'bathroom' : 1
         }, 
         {
            'id'       : 2,
            'img'      : ['test_accommodation_2_image_1.jpg', 'test_accommodation_2_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 2',
            'MaxNum'   : 3,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '20000',
            'lat'      : '37.444400',
            'long'     : '100.111100',
            'bed'      : 1,
            'bedroom'  : 1,
            'bathroom' : 2
         },
         {
            'id'       : 3,
            'img'      : ['test_accommodation_3_image_1.jpg', 'test_accommodation_3_image_2.jpg'],
            'location' : '강남구 개인실',
            'title'    : 'test accommodation 3',
            'MaxNum'   : 2,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '30000',
            'lat'      : '37.333300',
            'long'     : '100.333300',
            'bed'      : 1,
            'bedroom'  : 3,
            'bathroom' : 1
         }
        ])
        self.assertEqual(response.status_code, 200) 

    def test_get_accommodation_list_view_success_min_10000(self):
        response = client.get('/accommodation?checkin=2021-04-17&checkout=2021-04-20&guests=1&roomtype=entire&min=19000')
        self.assertEqual(response.json()["data"],
        [
            {
            'id'       : 2,
            'img'      : ['test_accommodation_2_image_1.jpg', 'test_accommodation_2_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 2',
            'MaxNum'   : 3,
            'grade'    : '0',
            'gradeNum' : 0,
            'price'    : '20000',
            'lat'      : '37.444400',
            'long'     : '100.111100',
            'bed'      : 1,
            'bedroom'  : 1,
            'bathroom' : 2
         }
        ])
        self.assertEqual(response.status_code, 200) 
    
    def test_get_accommodation_list_view_success_guests_4(self):
        response = client.get('/accommodation?checkin=2021-04-17&checkout=2021-04-20&guests=4')
        self.assertEqual(response.json()["data"],
        [
            {
            'id'       : 1,
            'img'      : ['test_accommodation_1_image_1.jpg', 'test_accommodation_1_image_2.jpg'],
            'location' : '강남구 집 전체',
            'title'    : 'test accommodation 1',
            'MaxNum'   : 5,
            'grade'    : '5.00',
            'gradeNum' : 1,
            'price'    : '16000',
            'lat'      : '37.511100',
            'long'     : '101.222200',
            'bed'      : 1,
            'bedroom'  : 2,
            'bathroom' : 1
         }
        ])
        self.assertEqual(response.status_code, 200) 

    def test_get_accommodation_list_view_success_guests_6(self):
        response = client.get('/accommodation?checkin=2021-04-17&checkout=2021-04-20&guests=6')
        self.assertEqual(response.json()["data"],[])
        self.assertEqual(response.status_code, 200) 
    
    

