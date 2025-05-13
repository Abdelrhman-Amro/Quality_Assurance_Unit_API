import json
import os
import random

from courses.models import Course, CourseAttachment, CourseFile
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from standards.models import AcademicYear

User = get_user_model()


class Command(BaseCommand):
    """
    - Create test data for courses using JSON files
        - for each ActiveYear1:3
            - Courses from couses.json
                - CourseFiles from course_file.json
                        - CourseAttachment1:3
        - for each ArchivedYear1:3
            - Courses from couses.json
                - CourseFiles from course_file.json
                        - CourseAttachment1:3
    """

    help = "Create test data for courses using JSON files"

    def handle(self, *args, **options):
        # Load course data from JSON files
        courses_data = self._load_json_file("couses.json")
        course_files_data = self._load_json_file("course_file.json")

        if not courses_data or not course_files_data:
            self.stdout.write(self.style.ERROR("Failed to load JSON data files. Aborting."))
            return

        # Get a professor user for assigning courses
        professors = User.objects.filter(role="PROFESSOR")
        if not professors.exists():
            self.stdout.write(self.style.WARNING("No professors found. Creating courses without professor assignment."))
            professor = None
        else:
            professor = professors.first()

        # get year by id
        # year = AcademicYear.objects.filter(id="32d51db1-883d-4653-9eba-4ab72fe34d44").first()
        # CREATE ACADEMIC YEAR
        year = AcademicYear.objects.create(
            title="2025-2030",
            start_date="2025-09-01",
            end_date="2030-06-30",
            status=AcademicYear.Status.ACTIVE,
        )
        self._create_courses_for_year(year, professor, courses_data, course_files_data)

        # # Get active academic years
        # active_years = AcademicYear.objects.filter(status=AcademicYear.Status.ACTIVE)
        # if not active_years.exists():
        #     self.stdout.write(
        #         self.style.WARNING(
        #             "No active academic years found. Skipping active year courses."
        #         )
        #     )
        # else:
        #     self.stdout.write(
        #         self.style.SUCCESS(
        #             f"Creating courses for {active_years.count()} active academic years"
        #         )
        #     )
        #     for year in active_years[:3]:  # Limit to 3 years as per docstring
        #         self._create_courses_for_year(
        #             year, professor, courses_data, course_files_data
        #         )

        # # Get archived academic years
        # archived_years = AcademicYear.objects.filter(
        #     status=AcademicYear.Status.ARCHIVED
        # )
        # if not archived_years.exists():
        #     self.stdout.write(
        #         self.style.WARNING(
        #             "No archived academic years found. Skipping archived year courses."
        #         )
        #     )
        # else:
        #     self.stdout.write(
        #         self.style.SUCCESS(
        #             f"Creating courses for {archived_years.count()} archived academic years"
        #         )
        #     )
        #     for year in archived_years[:3]:  # Limit to 3 years as per docstring
        #         self._create_courses_for_year(
        #             year, professor, courses_data, course_files_data
        #         )

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

    def _create_courses_for_year(self, academic_year, professor, courses_data, course_files_data):
        """Create courses for a specific academic year using JSON data"""
        # Use up to 3 courses from the JSON data
        for i, course_data in enumerate(courses_data):
            course = Course.objects.create(
                academic_year=academic_year,
                professor=professor,
                title=course_data["title"],
                code=course_data["code"],
                level=course_data["level"],
                semester=course_data["semester"],
                credit_hours=course_data["credit_hours"],
            )
            self.stdout.write(f"  Created course: {course.title}")
            self._create_course_files(course, course_files_data)

    def _create_course_files(self, course, course_files_data):
        """Create files for a specific course using JSON data"""
        # Use up to 3 files from the JSON data
        file_keys = list(course_files_data.keys())[:]
        for key in file_keys:
            file_title = course_files_data[key]
            course_file = CourseFile.objects.create(course=course, title=f"{file_title} for {course.title}")
            self.stdout.write(f"    Created course file: {course_file.title}")
            # self._create_course_attachments(course_file)

    # def _create_course_attachments(self, course_file):
    #     """Create attachments for a specific course file"""
    #     for i in range(1, 4):  # Create 3 attachments per file
    #         # Create a dummy file content
    #         content = ContentFile(f"This is test content for attachment {i} of {course_file.title}".encode())
    #         attachment = CourseAttachment.objects.create(course_file=course_file)
    #         # Save the file with a unique name
    #         attachment.file.save(f"attachment_{i}_{course_file.id}.txt", content)
    #         self.stdout.write(f"      Created attachment for {course_file.title}")
