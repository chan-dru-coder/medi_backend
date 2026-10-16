from django.db import migrations, models
import django.db.models.deletion
import django.core.validators

class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0012_alter_user_first_name_max_length")]
    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("is_superuser", models.BooleanField(default=False, help_text="Designates that this user has all permissions without explicitly assigning them.", verbose_name="superuser status")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("full_name", models.CharField(max_length=150)),
                ("role", models.CharField(choices=[("patient","Patient"),("doctor","Doctor")], max_length=20)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("profile_image", models.ImageField(blank=True, null=True, upload_to="profiles/")),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("groups", models.ManyToManyField(blank=True, related_name="custom_user_set", related_query_name="custom_user", to="auth.group")),
                ("user_permissions", models.ManyToManyField(blank=True, related_name="custom_user_set", related_query_name="custom_user", to="auth.permission")),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="DoctorProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("specialization", models.CharField(choices=[("Cardiologist","Cardiologist"),("Dermatologist","Dermatologist"),("Neurologist","Neurologist"),("Pediatrician","Pediatrician"),("Orthopedist","Orthopedist"),("General Physician","General Physician")], max_length=80)),
                ("qualification", models.CharField(max_length=150)),
                ("experience_years", models.PositiveIntegerField(default=0)),
                ("hospital", models.CharField(blank=True, max_length=200)),
                ("bio", models.TextField(blank=True)),
                ("rating", models.DecimalField(decimal_places=1, default=0, max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ("review_count", models.PositiveIntegerField(default=0)),
                ("profile_image", models.ImageField(blank=True, null=True, upload_to="doctors/")),
                ("consultation_fee", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="doctor_profile", to="accounts.user")),
            ],
        ),
        migrations.CreateModel(
            name="PatientProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("gender", models.CharField(blank=True, choices=[("male","Male"),("female","Female"),("other","Other")], max_length=20)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("address", models.TextField(blank=True)),
                ("emergency_contact", models.CharField(blank=True, max_length=100)),
                ("profile_image", models.ImageField(blank=True, null=True, upload_to="patients/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="patient_profile", to="accounts.user")),
            ],
        ),
    ]
