import jwt
import json
import unittest
from datetime               import date

from django.test            import Client, TestCase

from user.models            import User, SocialPlatform
from reservation.models     import Reservation, ReservationStatus
from accommodation.models   import Accommodation, Category, Image
from my_settings            import ALGORITHM, SECRET_KEY

class ReservationListViewTest(TestCase):
    def setUp(self):
        SocialPlatform.objects.create(
            name = 'kakao'
        )
        
        ReservationStatus.objects.create(
            code = 1,
            name = 'pending'
        )
        
        ReservationStatus.objects.create(
            code = 2,
            name = 'booked'
        )

        ReservationStatus.objects.create(
            code = 3,
            name = 'canceled'
        )

        User.objects.create(
            id                 = 1,
            email              = 'test_host@gmail.com',
            name               = 'test_host',
            profile_image      = 'profile_image.jpg',
            social_platform    = SocialPlatform.objects.get(name='kakao')
        )

        User.objects.create(
            id                 = 2,
            email              = 'test_user_with_reservation@gmail.com',
            name               = 'test_user_with_reservation',
            profile_image      = 'profile_image.jpg',
            social_platform    = SocialPlatform.objects.get(name='kakao')
        )

        User.objects.create(
            id                  = 3,
            email               = 'test_user_without_reservation@gmail.com',
            name                = 'test_user_without_reservation',
            profile_image       = 'profile_image.jpg',
            social_platform     = SocialPlatform.objects.get(name='kakao')
        )

        Category.objects.create(
            name        = '집 전체', 
            description = '집 전체를 사용하게 됩니다.'
        )

        Accommodation.objects.create(
            id                  = 1,
            category            = Category.objects.get(name='집 전체'), 
            user                = User.objects.get(email='test_host@gmail.com'),
            title               = 'test house', 
            address             = '서울특별시 강남구 테헤란로',
            latitude            = 37.5,
            longitude           = 127.05,
            description         = 'description',
            max_capacity        = 5,
            price               = 10000,
            cleaning_fee        = 1000,
            number_of_bed       = 1,
            number_of_bedroom   = 1,
            number_of_bathroom  = 1    
        )

        Image.objects.create(
            accommodation = Accommodation.objects.get(title='test house'),
            image_url     = 'house_image.jpg'
        )

        Reservation.objects.create(
            id              = 1,
            accommodation   = Accommodation.objects.get(id=1),
            user            = User.objects.get(email='test_user_with_reservation@gmail.com'),
            start_date      = '2021-01-16',
            end_date        = '2021-01-17',
            total_price     = 10000,
            total_guest     = 1,
            status          = ReservationStatus.objects.get(code=1)
        )

        Reservation.objects.create(
            id              = 2,
            accommodation   = Accommodation.objects.get(id=1),
            user            = User.objects.get(email='test_user_with_reservation@gmail.com'),
            start_date      = '2021-01-19',
            end_date        = '2021-01-20',
            total_price     = 10000,
            total_guest     = 1,
            status          = ReservationStatus.objects.get(code=2)
        )

        Reservation.objects.create(
            id              = 3,
            accommodation   = Accommodation.objects.get(id=1),
            user            = User.objects.get(email='test_user_with_reservation@gmail.com'),
            start_date      = '2021-04-19',
            end_date        = '2021-04-20',
            total_price     = 10000,
            total_guest     = 1,
            status          = ReservationStatus.objects.get(code=2)
        )
        
        Reservation.objects.create(
            id              = 4,
            accommodation   = Accommodation.objects.get(id=1),
            user            = User.objects.get(email='test_user_with_reservation@gmail.com'),
            start_date      = '2021-04-16',
            end_date        = '2021-04-17',
            total_price     = 10000,
            total_guest     = 1,
            status          = ReservationStatus.objects.get(code=3)
        )
    
    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        Accommodation.objects.all().delete()
        Image.objects.all().delete()
        Reservation.objects.all().delete()

    def test_reservation_list_get_sucess_with_reservation(self):
        client          = Client()
        self.maxDiff    = None
        user            = User.objects.get(id=2)
        access_token    = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM)
        headers         = {'HTTP_Authorization': access_token}
        
        response = client.get('/reservation', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
       
        self.assertEqual(response.json(), {
            'message': 'SUCESS',
            'results': {
                'canceledReservations': [{
                        'accommodationAddress' : '서울특별시 강남구 테헤란로',
                        'accommodationName'    : 'test house',
                        'endDate'              : '2021-04-17',
                        'startDate'            : '2021-04-16',
                        'thumbnailImage'       : 'house_image.jpg'
                }],
                'pastReservations': [{
                        'accommodationAddress' : '서울특별시 강남구 테헤란로',
                        'accommodationName'    : 'test house',
                        'endDate'              : '2021-01-20',
                        'startDate'            : '2021-01-19',
                        'thumbnailImage'       : 'house_image.jpg'
                }],
                'upcomingReservations': [{
                        'accommodationAddress' : '서울특별시 강남구 테헤란로',
                        'accommodationName'    : 'test house',
                        'endDate'              : '2021-04-20',
                        'startDate'            : '2021-04-19',
                        'thumbnailImage'       : 'house_image.jpg'
                }]
            }
        })
    
    def test_reservation_list_get_sucess_without_reservation(self):
        client          = Client()
        user            = User.objects.get(id=3)
        access_token    = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM)
        headers         = {'HTTP_Authorization': access_token}

        response = client.get('/reservation', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message':'NO_RESERVATION'})
        
