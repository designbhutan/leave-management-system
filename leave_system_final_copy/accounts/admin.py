from django.contrib import admin
from .models import StaffProfile

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "user", "department", "role", "annual_leave_entitlement")
    list_filter = ("role", "department")
    search_fields = ("employee_id", "user__username", "user__first_name", "user__last_name")
