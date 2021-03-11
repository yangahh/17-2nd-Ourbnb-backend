
from django.urls        import path
from reservation.views  import ReservationListView
from reservation.views  import PurchaseView

urlpatterns = [
    path('', ReservationListView.as_view()),
    path('/purchase', PurchaseView.as_view())
]
