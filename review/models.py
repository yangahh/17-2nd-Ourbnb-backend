from django.db          import models
from reservation.models import Reservation

class Review(models.Model):
    accommodation      = models.ForeignKey('accommodation.Accommodation', on_delete=models.CASCADE)
    user               = models.ForeignKey('user.User', on_delete=models.CASCADE)
    clean_rate         = models.DecimalField(max_digits=2, decimal_places=1)
    communication_rate = models.DecimalField(max_digits=2, decimal_places=1)
    checkin_rate       = models.DecimalField(max_digits=2, decimal_places=1)
    accuracy_rate      = models.DecimalField(max_digits=2, decimal_places=1)
    location_rate      = models.DecimalField(max_digits=2, decimal_places=1)
    value_rate         = models.DecimalField(max_digits=2, decimal_places=1)
    content            = models.TextField(max_length=2000)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
