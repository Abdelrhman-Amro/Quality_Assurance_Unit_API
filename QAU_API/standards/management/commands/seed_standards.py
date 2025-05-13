import json
import os
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from standards.models import AcademicYear, Attachment, Element, Pointer, Standard

User = get_user_model()


class Command(BaseCommand):
    """
    - Create test data for standards using standards.json
        - ActiveYear1:3
            - Standards from standards.json
                - Pointers from standards.json
                    - Elements from standards.json
                        - Attachments from standards.json
        - ArchivedYear1:3
            - Standards from standards.json
                - Pointers from standards.json
                    - Elements from standards.json
                        - Attachments from standards.json
    """

    help = "Create test data for standards using standards.json"

    def handle(self, *args, **options):
        # Load standards data from JSON file
        standards_data = self._load_json_file("standards.json")
        if not standards_data:
            self.stdout.write(self.style.ERROR("Failed to load standards.json. Aborting."))
            return

        # Get admin users for assignments
        admin_users = User.objects.filter(is_staff=True)[:3]
        if not admin_users.exists():
            self.stdout.write(self.style.WARNING("No admin users found. Creating standards without assignments."))

        year = AcademicYear.objects.filter(id="dae41c91-df3c-4cd0-8b3a-df292aa7b5f9").first()
        self._create_standards_for_year(year, standards_data, admin_users)

        # # Create active academic years
        # active_years = []
        # for i in range(1, 4):  # ActiveYear1:3
        #     current_year = timezone.now().year
        #     start_date = timezone.datetime(current_year, 9, 1).date()
        #     end_date = timezone.datetime(current_year + 1, 6, 30).date()

        #     year = AcademicYear.objects.create(
        #         status=AcademicYear.Status.ACTIVE,
        #         start_date=start_date,
        #         end_date=end_date,
        #     )
        #     active_years.append(year)
        #     self.stdout.write(self.style.SUCCESS(f"Created active academic year {i}: {year}"))

        # # Create archived academic years
        # archived_years = []
        # for i in range(1, 4):  # ArchivedYear1:3
        #     past_year = timezone.now().year - i
        #     start_date = timezone.datetime(past_year, 9, 1).date()
        #     end_date = timezone.datetime(past_year + 1, 6, 30).date()

        #     year = AcademicYear.objects.create(
        #         status=AcademicYear.Status.ARCHIVED,
        #         start_date=start_date,
        #         end_date=end_date,
        #     )
        #     archived_years.append(year)
        #     self.stdout.write(self.style.SUCCESS(f"Created archived academic year {i}: {year}"))

        # # Create standards, pointers, elements, and attachments for each year
        # for year in active_years + archived_years:
        #     self._create_standards_for_year(year, standards_data, admin_users)

        self.stdout.write(self.style.SUCCESS("Successfully created all test data"))

    def _load_json_file(self, filename):
        """Load data from a JSON file"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading {filename}: {str(e)}"))
            return None

    def _create_standards_for_year(self, academic_year, standards_data, admin_users):
        """Create standards for a specific academic year using JSON data"""
        for i, standard_data in enumerate(standards_data, 1):
            # Alternate between ACADEMIC and PRAGMATIC types
            # standard_type = (
            #     Standard.Type.ACADEMIC if i % 2 == 1 else Standard.Type.PRAGMATIC
            # )

            standard = Standard.objects.create(
                academic_year=academic_year,
                title=standard_data["title"],
                type=standard_data["type"],
            )

            # Assign users if available
            if admin_users.exists():
                for user in admin_users:
                    standard.assigned_to.add(user)

            self.stdout.write(self.style.SUCCESS(f"Created standard: {standard.title} for {academic_year}"))

            # Create pointers for each standard
            self._create_pointers_for_standard(standard, standard_data.get("pointers", []), admin_users)

    def _create_pointers_for_standard(self, standard, pointers_data, admin_users):
        """Create pointers for a specific standard using JSON data"""
        for pointer_data in pointers_data:
            pointer = Pointer.objects.create(
                standard=standard,
                title=pointer_data["title"],
            )
            self.stdout.write(self.style.SUCCESS(f"Created pointer: {pointer.title}"))

            # Create elements for each pointer
            self._create_elements_for_pointer(pointer, pointer_data.get("elements", []), admin_users)

    def _create_elements_for_pointer(self, pointer, elements_data, admin_users):
        """Create elements for a specific pointer using JSON data"""
        for element_data in elements_data:
            element = Element.objects.create(
                pointer=pointer,
                title=element_data["title"],
            )
            self.stdout.write(self.style.SUCCESS(f"Created element: {element.title}"))

            # Create attachments for each element
            self._create_attachments_for_element(element, element_data.get("attachments", []), admin_users)

    def _create_attachments_for_element(self, element, attachments_data, admin_users):
        """Create attachments for a specific element using JSON data"""
        for attachment_title in attachments_data:
            # Select a random user as uploader if available
            uploader = random.choice(list(admin_users)) if admin_users.exists() else None

            attachment = Attachment.objects.create(
                element=element,
                uploaded_by=uploader,
                title=attachment_title,
            )

            # Add shared_with users if available
            if admin_users.exists() and len(admin_users) > 1:
                # Share with users other than the uploader
                for user in admin_users:
                    if uploader and user != uploader:
                        attachment.shared_with.add(user)

            self.stdout.write(self.style.SUCCESS(f"Created attachment: {attachment.title}"))
