import random

from courses.models import Course, CourseAttachment, CourseFile
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from standards.models import AcademicYear

User = get_user_model()


class Command(BaseCommand):
    """
    - Create test data for courses
        - for each ActiveYear1:3
            - Course1:3
                - CourseFile1:3
                        - CourseAttachment1:3
        - for each ArchivedYear1:3
            - Course1:3
                - CourseFile1:3
                        - CourseAttachment1:3
    """

    help = "Create test data for courses"

    def handle(self, *args, **options):
        # Get a professor user for assigning courses
        professors = User.objects.filter(role="PROFESSOR")
        if not professors.exists():
            self.stdout.write(self.style.WARNING("No professors found. Creating courses without professor assignment."))
            professor = None
        else:
            professor = professors.first()

        # # Get active academic years
        # active_years = AcademicYear.objects.filter(status=AcademicYear.Status.ACTIVE)
        # if not active_years.exists():
        #     self.stdout.write(self.style.WARNING("No active academic years found. Skipping active year courses."))
        # else:
        #     self.stdout.write(self.style.SUCCESS(f"Creating courses for {active_years.count()} active academic years"))
        #     for year in active_years[:3]:  # Limit to 3 years as per docstring
        #         self._create_courses_for_year(year, professor)

        # # Get archived academic years
        # archived_years = AcademicYear.objects.filter(status=AcademicYear.Status.ARCHIVED)
        # if not archived_years.exists():
        #     self.stdout.write(self.style.WARNING("No archived academic years found. Skipping archived year courses."))
        # else:
        #     self.stdout.write(self.style.SUCCESS(f"Creating courses for {archived_years.count()} archived academic years"))
        #     for year in archived_years[:3]:  # Limit to 3 years as per docstring
        #         self._create_courses_for_year(year, professor)

        # get year by id
        year = AcademicYear.objects.filter(id="dae41c91-df3c-4cd0-8b3a-df292aa7b5f9").first()
        self._create_courses_for_year(year, professor)

        self.stdout.write(self.style.SUCCESS("Successfully created all test data"))

    def _create_courses_for_year(self, academic_year, professor):
        """Create courses for a specific academic year"""
        for i in range(1, 4):  # Create 3 courses per year
            course = Course.objects.create(
                academic_year=academic_year,
                professor=professor,
                title=f"Test Course {i} for {academic_year}",
                code=f"TC{academic_year.start_date.year}{i}{random.randint(100, 999)}",
                level=random.choice([1, 2, 3, 4]),
                semester=random.choice([1, 2]),
                credit_hours=random.choice([2, 3, 4]),
            )
            self.stdout.write(f"  Created course: {course.title}")
            self._create_course_files(course)

    def _create_course_files(self, course):
        """Create files for a specific course"""
        for i in range(1, 4):  # Create 3 files per course
            course_file = CourseFile.objects.create(course=course, title=f"File {i} for {course.title}")
            self.stdout.write(f"    Created course file: {course_file.title}")
            self._create_course_attachments(course_file)

    def _create_course_attachments(self, course_file):
        """Create attachments for a specific course file"""
        for i in range(1, 4):  # Create 3 attachments per file
            # Create a dummy file content
            content = ContentFile(f"This is test content for attachment {i} of {course_file.title}".encode())
            attachment = CourseAttachment.objects.create(course_file=course_file)
            # Save the file with a unique name
            attachment.file.save(f"attachment_{i}_{course_file.id}.txt", content)
            self.stdout.write(f"      Created attachment for {course_file.title}")
