from django.db import models

class User(models.Model):
    email           = models.EmailField(max_length=50) 
    name            = models.CharField(max_length=50) 
    phone_number    = models.CharField(max_length=20, null=True) 
    profile_image   = models.URLField(max_length=2000) 
    date_of_birth   = models.DateField(null=True) 
    social_platform = models.ForeignKey('SocialPlatform', on_delete=models.CASCADE)

    class Meta:
        db_table = 'users'

class SocialPlatform(models.Model):
    name  = models.CharField(max_length=50) 

    class Meta:
        db_table = 'social_platforms'