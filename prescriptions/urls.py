from django.urls import path
from .views import PrescriptionByAppointmentView, PrescriptionCreateView, PrescriptionDetailView

urlpatterns = [
    path("", PrescriptionCreateView.as_view()),
    path("<int:pk>/", PrescriptionDetailView.as_view()),
    path("appointment/<int:appointment_id>/", PrescriptionByAppointmentView.as_view()),
]
