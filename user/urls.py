from django.urls import path

from .views      import KakaoSigninView

urlpatterns = [
    path('/kakao/signin', KakaoSigninView.as_view()),
]
