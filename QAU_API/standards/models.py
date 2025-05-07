import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class AcademicYear(models.Model):
    """Model representing an academic year with active/archived status."""

    class Status(models.TextChoices):
        ARCHIVED = "ARCHIVED", "Archived"
        ACTIVE = "ACTIVE", "Active"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(max_length=8, choices=Status.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.start_date.year}-{self.end_date.year} ({self.get_status_display()})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"


class Standard(models.Model):
    """Model representing a standard with academic/pragmatic type."""

    class Type(models.TextChoices):
        ACADEMIC = "ACADEMIC", "Academic"
        PRAGMATIC = "PRAGMATIC", "Pragmatic"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="standards")
    assigned_to = models.ManyToManyField(User, related_name="assigned_standards", blank=True)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=Type.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Standard"
        verbose_name_plural = "Standards"


class Pointer(models.Model):
    """Model representing a pointer associated with a standard."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name="pointers")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pointer"
        verbose_name_plural = "Pointers"


class Element(models.Model):
    """Model representing an element associated with a pointer."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    pointer = models.ForeignKey(Pointer, on_delete=models.CASCADE, related_name="elements")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Element"
        verbose_name_plural = "Elements"


class Attachment(models.Model):
    """Model representing an attachment associated with an element."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name="attachments")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="uploaded_attachments", blank=True, null=True)
    shared_with = models.ManyToManyField(User, related_name="shared_attachments", blank=True)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="attachments/", blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"


class Request(models.Model):
    """Model representing a request associated with an attachment."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        CANCELED = "CANCELED", "Canceled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")
    made_on = models.ForeignKey(Attachment, on_delete=models.CASCADE, related_name="requests")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request from {self.requester} to {self.receiver} ({self.get_status_display()})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Request"
        verbose_name_plural = "Requests"
