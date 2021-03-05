import jwt
import json
import requests

from django.views           import View
from django.http            import JsonResponse

from my_settings            import SECRET_KEY, ALGORITHM
from .models                import User, SocialPlatform

class KakaoSigninView(View):
    def post(self, request):
        try:
            token = request.headers.get('Authorization')

            if not token:
                return JsonResponse({"message": "INVALID_SNS_TOKEN"}, status=400)

            kakao_user      = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {token}"})
            kakao_user_json = kakao_user.json()

            email         = kakao_user_json['kakao_account']['email']
            kakao_profile = kakao_user_json['kakao_account']['profile']
            name          = kakao_user_json['kakao_account']['profile']['nickname']
            profile_image = kakao_profile.get('thumbnail_image_url', 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png')

            user = User.objects.get_or_create(
                email           = email,
                social_platform = SocialPlatform.objects.get(name='kakao'),
                defaults = {
                    'name'          : name,
                    'profile_image' : profile_image
                }
            )[0]
            access_token = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({"message": "SUCCESS", "access_token": access_token}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except SocialPlatform.DoesNotExist:
            return JsonResponse({"message": "SOCIAL_PLATFORM_DOES_NOT_EXIST"}, status=400)



