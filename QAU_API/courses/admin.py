from django.contrib import admin
from django.utils.html import format_html

from .models import Course, CourseAttachment, CourseFile


class CourseAttachmentInline(admin.TabularInline):
    model = CourseAttachment
    extra = 1
    fields = ["file"]


class CourseFileInline(admin.TabularInline):
    model = CourseFile
    extra = 1
    fields = ["title"]
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "professor", "department", "academic_year", "created_at"]
    list_filter = ["academic_year", "professor", "department"]
    search_fields = ["title", "professor__username", "professor__email"]
    date_hierarchy = "created_at"
    inlines = [CourseFileInline]


@admin.register(CourseFile)
class CourseFileAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "attachment_count", "created_at"]
    list_filter = ["course", "created_at"]
    search_fields = ["title", "course__title"]
    date_hierarchy = "created_at"
    inlines = [CourseAttachmentInline]

    def attachment_count(self, obj):
        count = obj.course_attachments.count()
        return count if count > 0 else "-"

    attachment_count.short_description = "Attachments"


@admin.register(CourseAttachment)
class CourseAttachmentAdmin(admin.ModelAdmin):
    list_display = ["id", "course_file", "file_link", "created_at"]
    list_filter = ["course_file", "created_at"]
    search_fields = ["course_file__title"]
    date_hierarchy = "created_at"

    def file_link(self, obj):
        if obj.file and hasattr(obj.file, "url"):
            return format_html('<a href="{}" target="_blank">Download</a>', obj.file.url)
        return "-"

    file_link.short_description = "File"
