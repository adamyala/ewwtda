from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session

admin.AdminSite.site_header = "Easy Wins With The Django Admin"
admin.AdminSite.index_title = "EWWTDA Dashboard"


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_id",
        "object_repr",
        "action_flag",
        "change_message",
    ]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = [
        "session_key",
        "decoded_session_data",
        "expire_date",
    ]

    def decoded_session_data(self, record):
        return record.get_decoded()


def to_fieldset(title=None, description=None, style_classes=None, fields=None):
    style_classes = style_classes or {}

    fields = fields or []

    return (
        # title is called "name" in the docs
        title,
        # the below dict is called "field_options" in the docs
        {
            "classes": style_classes,
            "fields": fields,
            "description": description,
        },
    )
