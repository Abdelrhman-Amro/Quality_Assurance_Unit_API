# from django.contrib import admin
# from django.utils.translation import gettext_lazy as _

# from .models import AcademicYear, Standard, Pointer, Element, Attachment, Request


# class StandardInline(admin.TabularInline):
#     model = Standard
#     extra = 0
#     fields = ('title',)
#     show_change_link = True


# @admin.register(AcademicYear)
# class AcademicYearAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'status', 'start_date', 'end_date', 'created_at')
#     list_filter = ('status',)
#     search_fields = ('start_date', 'end_date')
#     readonly_fields = ('id', 'created_at', 'updated_at')
#     fieldsets = (
#         (None, {
#             'fields': ('status', 'start_date', 'end_date')
#         }),
#         (_('System Fields'), {
#             'fields': ('id', 'created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
#     inlines = [StandardInline]


# class PointerInline(admin.TabularInline):
#     model = Pointer
#     extra = 0
#     fields = ('title',)
#     show_change_link = True


# @admin.register(Standard)
# class StandardAdmin(admin.ModelAdmin):
#     list_display = ('title', 'academic_year', 'created_at')
#     list_filter = ('academic_year__status',)
#     search_fields = ('title', 'academic_year__start_date', 'academic_year__end_date')
#     readonly_fields = ('id', 'created_at', 'updated_at')
#     filter_horizontal = ('assigned_to',)
#     fieldsets = (
#         (None, {
#             'fields': ('title', 'academic_year', 'assigned_to')
#         }),
#         (_('System Fields'), {
#             'fields': ('id', 'created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
#     inlines = [PointerInline]


# class ElementInline(admin.TabularInline):
#     model = Element
#     extra = 0
#     fields = ('title',)
#     show_change_link = True


# @admin.register(Pointer)
# class PointerAdmin(admin.ModelAdmin):
#     list_display = ('title', 'standard', 'created_at')
#     list_filter = ('standard__academic_year__status',)
#     search_fields = ('title', 'standard__title')
#     readonly_fields = ('id', 'created_at', 'updated_at')
#     fieldsets = (
#         (None, {
#             'fields': ('title', 'standard')
#         }),
#         (_('System Fields'), {
#             'fields': ('id', 'created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
#     inlines = [ElementInline]


# class AttachmentInline(admin.TabularInline):
#     model = Attachment
#     extra = 0
#     fields = ('title', 'file', 'uploaded_by')
#     show_change_link = True


# @admin.register(Element)
# class ElementAdmin(admin.ModelAdmin):
#     list_display = ('title', 'pointer', 'created_at')
#     list_filter = ('pointer__standard__academic_year__status',)
#     search_fields = ('title', 'pointer__title', 'pointer__standard__title')
#     readonly_fields = ('id', 'created_at', 'updated_at')
#     fieldsets = (
#         (None, {
#             'fields': ('title', 'pointer')
#         }),
#         (_('System Fields'), {
#             'fields': ('id', 'created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
#     inlines = [AttachmentInline]


# class RequestInline(admin.TabularInline):
#     model = Request
#     extra = 0
#     fields = ('requester', 'receiver', 'status')
#     fk_name = 'made_on'
#     show_change_link = True


# @admin.register(Attachment)
# class AttachmentAdmin(admin.ModelAdmin):
#     list_display = ('title', 'element', 'uploaded_by', 'created_at')
#     list_filter = ('element__pointer__standard__academic_year__status', 'uploaded_by')
#     search_fields = ('title', 'element__title', 'uploaded_by__username')
#     readonly_fields = ('id', 'created_at', 'updated_at')
#     filter_horizontal = ('shared_with',)
#     fieldsets = (
#         (None, {
#             'fields': ('title', 'element', 'file')
#         }),
#         (_('Users'), {
#             'fields': ('uploaded_by', 'shared_with')
#         }),
#         (_('System Fields'), {
#             'fields': ('id', 'created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
#     inlines = [RequestInline]


# @admin.register(Request)
# class RequestAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'requester', 'receiver', 'made_on', 'status', 'created_at')
#     list_filter = ('status', 'requester', 'receiver')
#     search_fields = ('requester__username', 'receiver__username', 'made_on__title')
#     readonly_fields = ('id', 'created_at', 'updated_at')
#     fieldsets = (
#         (None, {
#             'fields': ('requester', 'receiver', 'made_on', 'status')
#         }),
#         (_('System Fields'), {
#             'fields': ('id', 'created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
#     actions = ['approve_requests', 'reject_requests', 'cancel_requests']

#     def approve_requests(self, request, queryset):
#         queryset.update(status=Request.Status.APPROVED)
#     approve_requests.short_description = _("Mark selected requests as approved")

#     def reject_requests(self, request, queryset):
#         queryset.update(status=Request.Status.REJECTED)
#     reject_requests.short_description = _("Mark selected requests as rejected")

#     def cancel_requests(self, request, queryset):
#         queryset.update(status=Request.Status.CANCELED)
#     cancel_requests.short_description = _("Mark selected requests as canceled")
