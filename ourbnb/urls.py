from django.urls    import path, include

urlpatterns = [
    path('accommodation', include('accommodation.urls')),
    path('user', include('user.urls'))
]