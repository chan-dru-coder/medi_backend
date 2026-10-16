from django.urls import path
from .views import DoctorAvailabilityView, DoctorDetailView, DoctorListView

urlpatterns = [
    path("", DoctorListView.as_view()),
    path("<int:pk>/", DoctorDetailView.as_view()),
    path("<int:doctor_id>/availability/", DoctorAvailabilityView.as_view()),
]
