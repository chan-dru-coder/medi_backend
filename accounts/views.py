from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from appointments.models import Appointment
from prescriptions.models import Prescription
from doctors.serializers import AppointmentSummarySerializer
from prescriptions.serializers import PrescriptionSummarySerializer
from .models import User
from .permissions import IsDoctor, IsPatient
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class PatientDashboardView(APIView):
    permission_classes = [IsPatient]
    def get(self, request):
        appointments = Appointment.objects.filter(patient=request.user).select_related(
            "doctor__user"
        ).order_by("appointment_date", "appointment_time")
        return Response({
            "upcoming_appointments": AppointmentSummarySerializer(
                appointments.filter(status__in=["pending", "accepted"]), many=True
            ).data,
            "pending_appointments": appointments.filter(status="pending").count(),
            "completed_appointments": appointments.filter(status="completed").count(),
            "recent_prescriptions": PrescriptionSummarySerializer(
                Prescription.objects.filter(patient=request.user).order_by("-created_at")[:5], many=True
            ).data,
        })

class DoctorDashboardView(APIView):
    permission_classes = [IsDoctor]
    def get(self, request):
        appointments = Appointment.objects.filter(doctor=request.user).select_related(
            "patient"
        ).order_by("appointment_date", "appointment_time")
        return Response({
            "today_appointments": AppointmentSummarySerializer(
                appointments.filter(appointment_date=timezone.localdate()), many=True
            ).data,
            "pending_appointments": appointments.filter(status="pending").count(),
            "accepted_appointments": appointments.filter(status="accepted").count(),
            "completed_appointments": appointments.filter(status="completed").count(),
        })
