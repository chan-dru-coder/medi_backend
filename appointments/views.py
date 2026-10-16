from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from .models import Appointment
from .permissions import IsDoctor, IsPatient
from .serializers import AppointmentSerializer

class AppointmentViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.select_related("patient", "doctor__user").all()
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_permissions(self):
        if self.action == "create":
            return [IsPatient()]
        if self.action in ["accept", "reject", "complete"]:
            return [IsDoctor()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "patient":
            return self.queryset.filter(patient=user)
        if user.role == "doctor":
            return self.queryset.filter(doctor__user=user)
        return self.queryset

    @action(detail=False, methods=["get"], url_path="my")
    def my_appointments(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    @action(detail=True, methods=["patch"])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        if appointment.patient != request.user:
            return Response({"success": False, "message": "You cannot cancel this appointment."}, status=403)
        if appointment.status in [Appointment.Status.COMPLETED, Appointment.Status.REJECTED, Appointment.Status.CANCELLED]:
            return Response({"success": False, "message": "This appointment cannot be cancelled."}, status=400)
        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(appointment).data)

    def _doctor_action(self, request, pk, new_status):
        appointment = get_object_or_404(self.queryset, pk=pk)
        if appointment.doctor.user != request.user:
            return Response({"success": False, "message": "You are not the assigned doctor."}, status=403)
        allowed = {
            Appointment.Status.ACCEPTED: [Appointment.Status.PENDING],
            Appointment.Status.REJECTED: [Appointment.Status.PENDING],
            Appointment.Status.COMPLETED: [Appointment.Status.ACCEPTED],
        }
        if appointment.status not in allowed[new_status]:
            return Response({"success": False, "message": f"Cannot change {appointment.status} to {new_status}."}, status=400)
        appointment.status = new_status
        appointment.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(appointment).data)

    @action(detail=True, methods=["patch"])
    def accept(self, request, pk=None):
        return self._doctor_action(request, pk, Appointment.Status.ACCEPTED)

    @action(detail=True, methods=["patch"])
    def reject(self, request, pk=None):
        return self._doctor_action(request, pk, Appointment.Status.REJECTED)

    @action(detail=True, methods=["patch"])
    def complete(self, request, pk=None):
        return self._doctor_action(request, pk, Appointment.Status.COMPLETED)

    @transaction.atomic
    def perform_create(self, serializer):
        doctor = serializer.validated_data["doctor"]
        appointment_date = serializer.validated_data["appointment_date"]
        appointment_time = serializer.validated_data["appointment_time"]

        # Lock the doctor's availability row for this exact slot. MySQL does not
        # support Django's conditional unique constraints, so this transaction
        # provides concurrency-safe double-booking protection when slots are
        # created through DoctorAvailability.
        from doctors.models import DoctorAvailability
        slot = DoctorAvailability.objects.select_for_update().filter(
            doctor=doctor,
            date=appointment_date,
            start_time=appointment_time,
            is_available=True,
        ).first()
        if not slot:
            raise serializers.ValidationError({"detail": "The selected appointment slot is not available."})

        if Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status__in=[Appointment.Status.PENDING, Appointment.Status.ACCEPTED],
        ).exists():
            raise serializers.ValidationError({"detail": "Appointment slot is already booked."})

        if Appointment.objects.filter(
            patient=self.request.user,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status__in=[Appointment.Status.PENDING, Appointment.Status.ACCEPTED],
        ).exists():
            raise serializers.ValidationError({"detail": "You already have an appointment at this time."})

        serializer.save()
