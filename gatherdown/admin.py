from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Event, Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "organization_link",
        "date",
        "image_preview",
        "duplicate_event",
    ]

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
