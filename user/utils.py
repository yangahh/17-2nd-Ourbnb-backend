import jwt
import json

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings import SECRET_KEY, ALGORITHM
from .models     import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        
        access_token = request.headers.get('Authorization')

        if not access_token:
            return JsonResponse({"message": "NEED_LOGIN"}, status=401)
        
        try:
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            login_user   = User.objects.get(id=payload['user'])
            request.user = login_user

            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)

    return wrapper
