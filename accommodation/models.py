from django.db   import models
from user.models import User

class Category(models.Model):
    name        = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

class Accommodation(models.Model):
    category           = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    user               = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title              = models.CharField(max_length=300)
    address            = models.CharField(max_length=200)
    latitude           = models.DecimalField(max_digits=9, decimal_places=6)
    longitude          = models.DecimalField(max_digits=9, decimal_places=6)
    description        = models.TextField()
    max_capacity       = models.IntegerField()
    price              = models.DecimalField(max_digits=10, decimal_places=2)
    cleaning_fee       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    number_of_bed      = models.IntegerField()
    number_of_bedroom  = models.IntegerField()
    number_of_bathroom = models.IntegerField()

    class Meta:
        db_table = 'accommodations'

class Image(models.Model):
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE)
    image_url     = models.URLField(max_length=2000)

    class Meta:
        db_table = 'images'

class UnavailableDate(models.Model):
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE)
    start_date    = models.DateField() 
    end_date      = models.DateField()       

    class Meta:
        db_table = 'unavailable_dates'
