from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import StaffProfile
from .forms import LeaveApplicationForm, ReviewLeaveForm
from .models import LeaveApplication, LeaveType

def profile_for(user):
    profile, _ = StaffProfile.objects.get_or_create(
        user=user,
        defaults={"employee_id": user.username}
    )
    return profile

def is_supervisor(user):
    return user.is_authenticated and profile_for(user).is_supervisor

def leave_summary(user):
    profile = profile_for(user)
    types = LeaveType.objects.filter(active=True).order_by("name")
    result = []
    for lt in types:
        entitlement = lt.annual_entitlement
        used = LeaveApplication.objects.filter(
            staff=user, leave_type=lt, status=LeaveApplication.APPROVED,
            start_date__year=timezone.localdate().year
        ).aggregate(total=Sum("days"))["total"] or Decimal("0")
        result.append({
            "type": lt,
            "entitlement": entitlement,
            "used": used,
            "balance": max(Decimal("0"), entitlement - used),
        })
    return result

@login_required
def dashboard(request):
    if is_supervisor(request.user):
        return redirect("supervisor_dashboard")
    applications = LeaveApplication.objects.filter(staff=request.user).select_related("leave_type", "reviewed_by")[:8]
    return render(request, "staff/dashboard.html", {
        "summary": leave_summary(request.user),
        "applications": applications,
        "profile": profile_for(request.user),
    })

@login_required
def apply_leave(request):
    if is_supervisor(request.user):
        messages.info(request, "Supervisors use the supervisor dashboard for staff review.")
        return redirect("supervisor_dashboard")

    if request.method == "POST":
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.staff = request.user
            app.days = form.cleaned_data["calculated_days"]
            app.save()
            messages.success(request, "Leave application submitted successfully.")
            return redirect("my_leaves")
    else:
        form = LeaveApplicationForm()
    return render(request, "staff/apply_leave.html", {"form": form})

@login_required
def my_leaves(request):
    qs = LeaveApplication.objects.filter(staff=request.user).select_related("leave_type", "reviewed_by")
    status = request.GET.get("status", "")
    if status in dict(LeaveApplication.STATUS_CHOICES):
        qs = qs.filter(status=status)
    return render(request, "staff/my_leaves.html", {
        "applications": qs,
        "current_status": status,
        "summary": leave_summary(request.user),
    })

@login_required
def supervisor_dashboard(request):
    if not is_supervisor(request.user):
        messages.error(request, "Supervisor access required.")
        return redirect("dashboard")

    qs = LeaveApplication.objects.select_related("staff", "leave_type", "reviewed_by").all()

    person = request.GET.get("person", "").strip()
    status = request.GET.get("status", "").strip()
    leave_type = request.GET.get("leave_type", "").strip()
    start = request.GET.get("start", "").strip()
    end = request.GET.get("end", "").strip()

    if person:
        qs = qs.filter(
            Q(staff__username__icontains=person) |
            Q(staff__first_name__icontains=person) |
            Q(staff__last_name__icontains=person) |
            Q(staff__profile__employee_id__icontains=person)
        )
    if status in dict(LeaveApplication.STATUS_CHOICES):
        qs = qs.filter(status=status)
    if leave_type.isdigit():
        qs = qs.filter(leave_type_id=int(leave_type))
    if start:
        qs = qs.filter(start_date__gte=start)
    if end:
        qs = qs.filter(end_date__lte=end)

    return render(request, "supervisor/dashboard.html", {
        "applications": qs,
        "leave_types": LeaveType.objects.filter(active=True).order_by("name"),
        "statuses": LeaveApplication.STATUS_CHOICES,
        "filters": {
            "person": person, "status": status, "leave_type": leave_type,
            "start": start, "end": end,
        },
        "pending_count": LeaveApplication.objects.filter(status=LeaveApplication.PENDING).count(),
        "staff_count": StaffProfile.objects.filter(role=StaffProfile.ROLE_STAFF).count(),
    })

@login_required
def review_leave(request, pk):
    if not is_supervisor(request.user):
        messages.error(request, "Supervisor access required.")
        return redirect("dashboard")

    application = get_object_or_404(
        LeaveApplication.objects.select_related("staff", "leave_type"), pk=pk
    )
    if application.status != LeaveApplication.PENDING:
        messages.info(request, "This leave application has already been reviewed.")
        return redirect("supervisor_dashboard")

    if request.method == "POST":
        form = ReviewLeaveForm(request.POST)
        if form.is_valid():
            application.status = form.cleaned_data["decision"]
            application.supervisor_remarks = form.cleaned_data["remarks"]
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save()
            messages.success(request, f"Leave {application.status.lower()} successfully.")
            return redirect("supervisor_dashboard")
    else:
        form = ReviewLeaveForm()
    return render(request, "supervisor/review_leave.html", {
        "application": application,
        "form": form,
    })

@login_required
def cancel_review(request, pk):
    if not is_supervisor(request.user):
        return redirect("dashboard")
    app = get_object_or_404(LeaveApplication, pk=pk)
    if request.method == "POST":
        app.status = LeaveApplication.PENDING
        app.reviewed_by = None
        app.reviewed_at = None
        app.supervisor_remarks = ""
        app.save()
        messages.success(request, "Review was returned to Pending.")
    return redirect("supervisor_dashboard")
