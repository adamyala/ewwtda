from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from core.admin import to_fieldset

from .models import Event, Organization


@admin.action(description="Send event reminder ✉️")
def send_event_reminder(model_admin, request, queryset):
    for event in queryset:
        print(f"send a reminder for {event}")
    messages.success(request, f"Reminders sent for {queryset.count()} event(s).")


class EventInline(admin.TabularInline):
    model = Event


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]

    inlines = [EventInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "organization_link",
        "date",
        "image_preview",
        "duplicate_event",
    ]

    actions = [send_event_reminder]

    # filter_horizontal = ["attendees"]

    # fields = ["name", "date"]

    # fieldsets = [
    #     (
    #         "Event Details",
    #         {
    #             "classes": {},
    #             "fields": ["name", "date", "image_url"],
    #             "description": None,
    #         },
    #     ),
    #     (
    #         "Related Records",
    #         {
    #             "classes": {},
    #             "fields": ["organization", "attendees"],
    #             "description": None,
    #         },
    #     ),
    #     ("Files", {"classes": {}, "fields": ["file_download"], "description": None}),
    # ]

    readonly_fields = ["file_download"]

    # details_fieldset = to_fieldset(title="Event Details", fields=["name", "date", "image_url"])
    # related_records_fieldset = to_fieldset(title="Related Records", fields=["organization", "attendees"])
    # files_fieldset = to_fieldset(title="Files", fields=["file_download"])
    # fieldsets = [details_fieldset, related_records_fieldset, files_fieldset]

    def image_preview(self, record):
        image_tag = f'<img src="{record.image_url}"/>'
        safe_image_tag = mark_safe(image_tag)
        return safe_image_tag

    def organization_link(self, record):
        organization_path = f"/admin/gatherdown/organization/{record.organization.id}"
        link_tag = f'<a href="{organization_path}">{record.organization.name}</a>'
        safe_link_tag = mark_safe(link_tag)
        return safe_link_tag

    def duplicate_event(self, record):
        new_event_path = "/admin/gatherdown/event/add?"
        params = f"organization={record.organization.id}&name={record.name}&image_url={record.image_url}"
        duplicate_path = new_event_path + params
        link_tag = f'<a href="{duplicate_path}">Duplicate</a>'
        safe_link_tag = mark_safe(link_tag)
        return safe_link_tag
