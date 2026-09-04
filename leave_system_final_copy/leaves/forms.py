from datetime import timedelta
from django import forms
from django.utils import timezone
from .models import LeaveApplication, PublicHoliday

def working_leave_days(start, end):
    holidays=set(PublicHoliday.objects.filter(date__range=(start,end)).values_list("date",flat=True))
    count=0
    current=start
    while current <= end:
        if current.weekday() < 5 and current not in holidays:
            count += 1
        current += timedelta(days=1)
    return count

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model=LeaveApplication
        fields=["leave_type","start_date","end_date","reason"]
        widgets={"start_date":forms.DateInput(attrs={"type":"date"}),"end_date":forms.DateInput(attrs={"type":"date"}),"reason":forms.Textarea(attrs={"rows":4,"placeholder":"Reason for leave"})}
    def clean(self):
        cleaned=super().clean(); start=cleaned.get("start_date"); end=cleaned.get("end_date")
        if start and end:
            if end < start: raise forms.ValidationError("End date cannot be before start date.")
            if start < timezone.localdate(): raise forms.ValidationError("Leave cannot start in the past.")
            days=working_leave_days(start,end)
            if days == 0: raise forms.ValidationError("The selected period contains only weekends/public holidays. Please select a working day.")
            cleaned["calculated_days"]=days
        return cleaned

class ReviewLeaveForm(forms.Form):
    decision=forms.ChoiceField(choices=[(LeaveApplication.APPROVED,"Approve"),(LeaveApplication.REJECTED,"Reject")],widget=forms.RadioSelect)
    remarks=forms.CharField(required=False,widget=forms.Textarea(attrs={"rows":4,"placeholder":"Supervisor remarks"}))
