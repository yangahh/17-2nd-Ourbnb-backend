from django.urls import path

from .views      import AccommodationListView, AccomodationDetailView, FileUploadView

urlpatterns = [
    path('', AccommodationListView.as_view()),
    path('/<int:accommodation_id>', AccomodationDetailView.as_view()),
    path('/file', FileUploadView.as_view()),
]

