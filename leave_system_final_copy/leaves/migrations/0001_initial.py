from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="LeaveType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("annual_entitlement", models.DecimalField(decimal_places=2, default=30, max_digits=6)),
                ("description", models.TextField(blank=True)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="LeaveApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("days", models.DecimalField(decimal_places=2, max_digits=6)),
                ("reason", models.TextField()),
                ("status", models.CharField(choices=[("PENDING","Pending"),("APPROVED","Approved"),("REJECTED","Rejected")], default="PENDING", max_length=20)),
                ("supervisor_remarks", models.TextField(blank=True)),
                ("applied_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("leave_type", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="applications", to="leaves.leavetype")),
                ("reviewed_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="reviewed_leave_applications", to=settings.AUTH_USER_MODEL)),
                ("staff", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="leave_applications", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-applied_at"]},
        ),
    ]
