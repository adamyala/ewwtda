from django.contrib import admin

from .models import Event, Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "organization",
        "name",
        "date",
        "image_url",
    ]
