from django.urls import path

from .views      import AccomodationDetailView

urlpatterns = [
    path('/<int:accommodation_id>', AccomodationDetailView.as_view()),
]

