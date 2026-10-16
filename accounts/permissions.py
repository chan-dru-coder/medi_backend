from rest_framework.permissions import BasePermission

class IsPatient(BasePermission):
    message = "Patient access is required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "patient")

class IsDoctor(BasePermission):
    message = "Doctor access is required."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "doctor")
