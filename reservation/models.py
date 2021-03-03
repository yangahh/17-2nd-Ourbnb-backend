from django.db            import models
from accommodation.models import Accommodation
from user.models          import User

class Reservation(models.Model):
    accommodation = models.ForeignKey('accommodation.Accommodation', on_delete=models.SET_NULL, null=True)
    user          = models.ForeignKey('user.User', on_delete=models.CASCADE)
    start_date    = models.DateField()
    end_date      = models.DateField()
    total_price   = models.DecimalField(max_digits=10, decimal_places=2)
    total_guest   = models.IntegerField()
    status        = models.ForeignKey('ReservationStatus', on_delete=models.CASCADE)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reservations'

class ReservationStatus(models.Model):    
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'reservation_status'