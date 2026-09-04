from django.contrib import admin
from .models import LeaveApplication, LeaveType, PublicHoliday

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display=("name","annual_entitlement","active")
    list_filter=("active",)
    search_fields=("name",)

@admin.register(PublicHoliday)
class PublicHolidayAdmin(admin.ModelAdmin):
    list_display=("date","name")
    list_filter=("date",)
    search_fields=("name",)

@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display=("staff","leave_type","start_date","end_date","days","status","reviewed_by","applied_at")
    list_filter=("status","leave_type","start_date")
    search_fields=("staff__username","staff__first_name","staff__last_name","reason")
