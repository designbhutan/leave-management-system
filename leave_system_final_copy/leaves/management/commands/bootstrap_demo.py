from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from accounts.models import StaffProfile
from leaves.models import LeaveType

class Command(BaseCommand):
    help = "Create/update a supervisor and sample staff accounts and default leave types."

    def add_arguments(self, parser):
        parser.add_argument("--supervisor-username", default="supervisor")
        parser.add_argument("--supervisor-password", default="ChangeMe123!")
        parser.add_argument("--supervisor-email", default="supervisor@example.com")
        parser.add_argument("--create-demo-staff", action="store_true")

    def handle(self, *args, **opts):
        su = opts["supervisor_username"]
        sp = opts["supervisor_password"]
        if len(sp) < 8:
            raise CommandError("Supervisor password must be at least 8 characters.")

        supervisor, created = User.objects.get_or_create(username=su, defaults={
            "email": opts["supervisor_email"], "first_name": "Leave", "last_name": "Supervisor"
        })
        supervisor.email = opts["supervisor_email"]
        supervisor.set_password(sp)
        supervisor.save()

        profile, _ = StaffProfile.objects.get_or_create(user=supervisor, defaults={
            "employee_id": "SUP-001", "role": StaffProfile.ROLE_SUPERVISOR
        })
        profile.role = StaffProfile.ROLE_SUPERVISOR
        profile.save()

        annual, _ = LeaveType.objects.get_or_create(name="Annual Leave", defaults={"annual_entitlement": 21})
        annual.annual_entitlement=21
        annual.active=True
        annual.save()
        LeaveType.objects.exclude(name="Annual Leave").delete()

        if opts["create_demo_staff"]:
            for username, employee_id, first, last in [
                ("staff001", "EMP-001", "Demo", "Staff"),
                ("staff002", "EMP-002", "Sample", "Employee"),
            ]:
                user, _ = User.objects.get_or_create(username=username)
                user.first_name, user.last_name = first, last
                user.set_password("ChangeMe123!")
                user.save()
                StaffProfile.objects.update_or_create(
                    user=user,
                    defaults={"employee_id": employee_id, "role": StaffProfile.ROLE_STAFF}
                )

        self.stdout.write(self.style.SUCCESS("Leave Management System bootstrap completed."))
        self.stdout.write("Supervisor username: " + su)
        self.stdout.write("Supervisor password: " + sp)
        if opts["create_demo_staff"]:
            self.stdout.write("Demo staff: staff001 / ChangeMe123!, staff002 / ChangeMe123!")
