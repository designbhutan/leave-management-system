from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="StaffProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_id", models.CharField(max_length=50, unique=True)),
                ("department", models.CharField(blank=True, max_length=150)),
                ("phone", models.CharField(blank=True, max_length=50)),
                ("role", models.CharField(choices=[("STAFF","Staff"),("SUPERVISOR","Supervisor")], default="STAFF", max_length=20)),
                ("annual_leave_entitlement", models.DecimalField(decimal_places=2, default=30, max_digits=6)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
