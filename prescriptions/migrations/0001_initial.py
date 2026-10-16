from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [("accounts","0001_initial"), ("appointments","0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Prescription",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("medical_notes", models.TextField(blank=True)),
                ("prescription", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("appointment", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="prescription_record", to="appointments.appointment")),
                ("doctor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="prescriptions", to="accounts.doctorprofile")),
                ("patient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="prescriptions", to="accounts.user")),
            ],
        ),
    ]
