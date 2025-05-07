import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from standards.models import AcademicYear, Attachment, Element, Pointer, Standard

User = get_user_model()


class Command(BaseCommand):
    """
    - Create test data for standards
        - ActiveYear1:3
            - Standard1:3
                - Pointer1:3
                    - Element1:3
                        - Attachment1:3
        - ArchivedYear1:3
            - Standard1:3
                - Pointer1:3
                    - Element1:3
                        - Attachment1:3
    """

    help = "Create test data for standards"

    def handle(self, *args, **options):
        # Get admin users for assignments
        admin_users = User.objects.filter(is_staff=True)[:3]
        if not admin_users.exists():
            self.stdout.write(self.style.WARNING("No admin users found. Creating standards without assignments."))

        # Create active academic years
        active_years = []
        for i in range(1, 4):  # ActiveYear1:3
            current_year = timezone.now().year
            start_date = timezone.datetime(current_year, 9, 1).date()
            end_date = timezone.datetime(current_year + 1, 6, 30).date()

            year = AcademicYear.objects.create(
                status=AcademicYear.Status.ACTIVE,
                start_date=start_date,
                end_date=end_date,
            )
            active_years.append(year)
            self.stdout.write(self.style.SUCCESS(f"Created active academic year {i}: {year}"))

        # Create archived academic years
        archived_years = []
        for i in range(1, 4):  # ArchivedYear1:3
            past_year = timezone.now().year - i
            start_date = timezone.datetime(past_year, 9, 1).date()
            end_date = timezone.datetime(past_year + 1, 6, 30).date()

            year = AcademicYear.objects.create(
                status=AcademicYear.Status.ARCHIVED,
                start_date=start_date,
                end_date=end_date,
            )
            archived_years.append(year)
            self.stdout.write(self.style.SUCCESS(f"Created archived academic year {i}: {year}"))

        # Create standards, pointers, elements, and attachments for each year
        for year_index, year in enumerate(active_years + archived_years):
            for i in range(1, 4):  # Standard1:3
                standard_type = random.choice([Standard.Type.ACADEMIC, Standard.Type.PRAGMATIC])
                standard = Standard.objects.create(
                    academic_year=year,
                    title=f"Standard {i} for {year}",
                    type=standard_type,
                )

                # Assign users if available
                if admin_users.exists():
                    for user in admin_users:
                        standard.assigned_to.add(user)

                self.stdout.write(self.style.SUCCESS(f"Created standard {i} for {year}"))

                # Create pointers for each standard
                for j in range(1, 4):  # Pointer1:3
                    pointer = Pointer.objects.create(standard=standard, title=f"Pointer {j} for Standard {i}")
                    self.stdout.write(self.style.SUCCESS(f"Created pointer {j} for standard {i}"))

                    # Create elements for each pointer
                    for k in range(1, 4):  # Element1:3
                        element = Element.objects.create(pointer=pointer, title=f"Element {k} for Pointer {j}")
                        self.stdout.write(self.style.SUCCESS(f"Created element {k} for pointer {j}"))

                        # Create attachments for each element
                        for l in range(1, 4):  # Attachment1:3
                            # Select a random user as uploader if available
                            uploader = random.choice(list(admin_users)) if admin_users.exists() else None

                            attachment = Attachment.objects.create(
                                element=element,
                                uploaded_by=uploader,
                                title=f"Attachment {l} for Element {k}",
                            )

                            # Add shared_with users if available
                            if admin_users.exists() and len(admin_users) > 1:
                                # Share with users other than the uploader
                                for user in admin_users:
                                    if uploader and user != uploader:
                                        attachment.shared_with.add(user)

                            self.stdout.write(self.style.SUCCESS(f"Created attachment {l} for element {k}"))

        self.stdout.write(self.style.SUCCESS("Successfully created all test data"))
