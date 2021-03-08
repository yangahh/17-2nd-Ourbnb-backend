from django.urls        import path,include
from reservation.views  import ReservationListView

urlpatterns = [
    path('', ReservationListView.as_view())
]
