from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from appointments.models import Appointment
from .models import Prescription
from .serializers import PrescriptionSerializer

class PrescriptionCreateView(generics.CreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        appointment = get_object_or_404(
            Appointment.objects.select_related("doctor__user", "patient"),
            pk=self.request.data.get("appointment")
        )
        if self.request.user.role != "doctor" or appointment.doctor.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only the assigned doctor can create a prescription.")
        if appointment.status != Appointment.Status.COMPLETED:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"appointment": "Prescription can only be created for a completed appointment."})
        serializer.save(patient=appointment.patient, doctor=appointment.doctor)

class PrescriptionDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Prescription.objects.select_related("patient", "doctor__user", "appointment")

    def get_object(self):
        obj = super().get_object()
        if self.request.user.role == "patient" and obj.patient != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        if self.request.user.role == "doctor" and obj.doctor.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        return obj

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.role != "doctor":
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only doctors can edit prescriptions.")
        return super().update(request, *args, **kwargs)

class PrescriptionByAppointmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, appointment_id):
        appointment = get_object_or_404(
            Appointment.objects.select_related("doctor__user", "patient"), pk=appointment_id
        )
        if request.user not in [appointment.patient, appointment.doctor.user]:
            return Response({"detail": "You do not have access to this prescription."}, status=403)
        prescription = get_object_or_404(Prescription, appointment=appointment)
        return Response(PrescriptionSerializer(prescription).data)
