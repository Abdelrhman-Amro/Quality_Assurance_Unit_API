from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """
    - Create test data for users
        - Admin1:5
        - Professor1:5
        - Supervisor1:5
        - TA1:10
    """

    help = "Create test data for users"

    def handle(self, *args, **options):
        # Default password for all test users
        default_password = "password123"

        # Create Admin users (Admin1-5)
        self.stdout.write(self.style.NOTICE("Creating Admin users..."))
        for i in range(1, 6):
            username = f"Admin{i}"
            email = f"admin{i}@example.com"
            User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": User.Role.ADMIN,
                    "first_name": f"AdminFirstName{i}",
                    "last_name": f"AdminLastName{i}",
                },
            )
            # Set password for newly created users
            user = User.objects.get(username=username)
            user.set_password(default_password)
            user.save()

        # Create Professor users (Professor1-5)
        self.stdout.write(self.style.NOTICE("Creating Professor users..."))
        for i in range(1, 6):
            username = f"Professor{i}"
            email = f"professor{i}@example.com"
            User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": User.Role.PROFESSOR,
                    "first_name": f"ProfessorFirstName{i}",
                    "last_name": f"ProfessorLastName{i}",
                },
            )
            # Set password for newly created users
            user = User.objects.get(username=username)
            user.set_password(default_password)
            user.save()

        # Create Supervisor users (Supervisor1-5)
        self.stdout.write(self.style.NOTICE("Creating Supervisor users..."))
        for i in range(1, 6):
            username = f"Supervisor{i}"
            email = f"supervisor{i}@example.com"
            User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": User.Role.SUPERVISOR,
                    "first_name": f"SupervisorFirstName{i}",
                    "last_name": f"SupervisorLastName{i}",
                },
            )
            # Set password for newly created users
            user = User.objects.get(username=username)
            user.set_password(default_password)
            user.save()

        # Create TA users (TA1-10)
        self.stdout.write(self.style.NOTICE("Creating TA users..."))
        for i in range(1, 11):
            username = f"TA{i}"
            email = f"ta{i}@example.com"
            User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": User.Role.TA,
                    "first_name": f"TAFirstName{i}",
                    "last_name": f"TALastName{i}",
                },
            )
            # Set password for newly created users
            user = User.objects.get(username=username)
            user.set_password(default_password)
            user.save()

        self.stdout.write(self.style.SUCCESS("Successfully created all test data"))
