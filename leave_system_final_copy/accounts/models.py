from django.contrib.auth.models import User
from django.db import models

class StaffProfile(models.Model):
    ROLE_STAFF = "STAFF"
    ROLE_SUPERVISOR = "SUPERVISOR"
    ROLE_CHOICES = [
        (ROLE_STAFF, "Staff"),
        (ROLE_SUPERVISOR, "Supervisor"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STAFF)
    annual_leave_entitlement = models.DecimalField(max_digits=6, decimal_places=2, default=30)

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"

    @property
    def is_supervisor(self):
        return self.role == self.ROLE_SUPERVISOR
