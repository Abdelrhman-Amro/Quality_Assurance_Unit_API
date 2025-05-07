from django.contrib import admin
from django.utils.html import format_html

from .models import AcademicYear, Attachment, Element, Pointer, Request, Standard


class PointerInline(admin.TabularInline):
    model = Pointer
    extra = 1
    fields = ("title",)


class ElementInline(admin.TabularInline):
    model = Element
    extra = 1
    fields = ("title",)


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1
    fields = ("title", "file", "uploaded_by")
    readonly_fields = ("uploaded_at",)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("__str__", "status", "start_date", "end_date", "created_at")
    list_filter = ("status",)
    search_fields = ("start_date", "end_date")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("status", "start_date", "end_date")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "academic_year", "created_at")
    list_filter = ("type", "academic_year")
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("assigned_to",)
    inlines = [PointerInline]
    fieldsets = (
        (None, {"fields": ("title", "type", "academic_year", "assigned_to")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Pointer)
class PointerAdmin(admin.ModelAdmin):
    list_display = ("title", "standard", "created_at")
    list_filter = ("standard",)
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [ElementInline]
    fieldsets = (
        (None, {"fields": ("title", "standard")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("title", "pointer", "created_at")
    list_filter = ("pointer",)
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [AttachmentInline]
    fieldsets = (
        (None, {"fields": ("title", "pointer")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("title", "element", "uploaded_by", "file_link", "uploaded_at")
    list_filter = ("element", "uploaded_by", "uploaded_at")
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at", "uploaded_at")
    filter_horizontal = ("shared_with",)
    fieldsets = (
        (None, {"fields": ("title", "element", "file", "uploaded_by", "shared_with")}),
        (
            "Timestamps",
            {
                "fields": ("uploaded_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.file.url)
        return "-"

    file_link.short_description = "File"


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "status",
        "requester",
        "receiver",
        "made_on",
        "created_at",
    )
    list_filter = ("status", "requester", "receiver")
    search_fields = ("requester__username", "receiver__username")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("requester", "receiver", "made_on", "status")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
