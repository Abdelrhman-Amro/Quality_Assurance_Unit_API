import uuid

from django.contrib.auth import get_user_model
from django.db import models
from standards.models import AcademicYear

User = get_user_model()


class Course(models.Model):
    """
    Model representing a course taught by a professor in a specific academic year.
    """

    class Level(models.IntegerChoices):
        FIRST = 1, "1"
        SECOND = 2, "2"
        THIRD = 3, "3"
        FOURTH = 4, "4"

    class Semester(models.IntegerChoices):
        FIRST = 1, "1"
        SECOND = 2, "2"

    class CreditHours(models.IntegerChoices):
        ZERO = 0, "0"
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"

    class Department(models.TextChoices):
        ARTIFICIAL_INTELLIGENCE = "AI", "Artificial Intelligence"
        COMPUTER_SCIENCE = "CS", "Computer Science"
        NETWORK = "NT", "Network"
        INFORMATION_SYSTEMS = "IS", "Information Systems"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="courses")
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="courses", null=True)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    level = models.IntegerField(choices=Level.choices)
    semester = models.IntegerField(choices=Semester.choices)
    credit_hours = models.IntegerField(choices=CreditHours.choices)
    department = models.CharField(max_length=50, choices=Department.choices, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class CourseFile(models.Model):
    """
    Model representing a file associated with a course.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="files")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Course File"
        verbose_name_plural = "Course Files"


class CourseAttachment(models.Model):
    """
    Model representing an attachment associated with a course file.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    course_file = models.ForeignKey(CourseFile, on_delete=models.CASCADE, related_name="course_attachments")
    file = models.FileField(upload_to="course_files/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Attachment for {self.course_file.title}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Course File Attachment"
        verbose_name_plural = "Course File Attachments"
