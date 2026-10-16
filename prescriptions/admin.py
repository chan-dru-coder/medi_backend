from django.contrib import admin
from .models import Prescription
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "appointment", "patient", "doctor", "created_at")
    search_fields = ("patient__email", "patient__full_name", "doctor__user__full_name")
