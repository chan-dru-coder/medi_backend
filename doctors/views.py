from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import DoctorProfile
from .models import DoctorAvailability
from .serializers import DoctorListSerializer, DoctorAvailabilitySerializer

class DoctorListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = DoctorListSerializer

    def get_queryset(self):
        qs = DoctorProfile.objects.select_related("user").all()
        search = self.request.query_params.get("search")
        specialization = self.request.query_params.get("specialization")
        if search:
            qs = qs.filter(
                Q(user__full_name__icontains=search) |
                Q(specialization__icontains=search) |
                Q(qualification__icontains=search) |
                Q(hospital__icontains=search)
            )
        if specialization and specialization != "All Specializations":
            qs = qs.filter(specialization__iexact=specialization)
        return qs.order_by("-rating", "user__full_name")

class DoctorDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = DoctorListSerializer
    queryset = DoctorProfile.objects.select_related("user").all()

class DoctorAvailabilityView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = DoctorAvailabilitySerializer
    def get_queryset(self):
        return DoctorAvailability.objects.filter(
            doctor_id=self.kwargs["doctor_id"], is_available=True
        ).order_by("date", "start_time")
