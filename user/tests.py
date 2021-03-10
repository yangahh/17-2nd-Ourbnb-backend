import unittest

from django.test   import TestCase
from django.test   import Client
from unittest.mock import patch, MagicMock

from .models       import SocialPlatform

class KakaoSigninTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SocialPlatform.objects.create(name='kakao')

    @patch('user.views.requests')
    def test_kakaosigninview_post_success(self, mock_requests):
        client = Client()

        class MockedRequestsResponse:
            def json(self):
                return {
                    'kakao_account': {
                        'email' : 'test@gmail.com',
                        'profile' : {
                            'nickname': 'test',
                            'thumbnail_image_url': 'http://asdf'
                        }
                    }
                }
                
        mock_requests.get = MagicMock(return_value = MockedRequestsResponse())
        headers  = {'HTTP_Authorization': 'fake_token'}
        response = client.post('/user/kakao/signin', content_type='applications/json', **headers)

        self.assertEqual(response.status_code, 200)

    @patch('user.views.requests')
    def test_kakaosigninview_post_invalid_keys(self, mock_requests):
        client = Client()

        class MockedRequestsResponse:
            def json(self):
                return {
                    'kakao_account': {
                        'email' : 'test@gmail.com',
                        'profile' : {
                            'name': 'test',
                            'thumbnail_image_url': 'http://asdf'
                        }
                    }
                }
                
        mock_requests.get = MagicMock(return_value = MockedRequestsResponse())
        headers  = {'HTTP_Authorization': 'fake_token'}
        response = client.post('/user/kakao/signin', content_type='applications/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'KEY_ERROR'})


    @patch('user.views.requests')
    def test_kakaosigninview_post_invalid_sns_token(self, mock_requests):
        client = Client()

        class MockedRequestsResponse:
            def json(self):
                return {
                    'kakao_account': {
                        'email' : 'test@gmail.com',
                        'profile' : {
                            'nickname': 'test',
                            'thumbnail_image_url': 'http://asdf'
                        }
                    }
                }
                
        mock_requests.get = MagicMock(return_value = MockedRequestsResponse())
        response = client.post('/user/kakao/signin')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_SNS_TOKEN'})
