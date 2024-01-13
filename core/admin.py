from django.contrib import admin
from django.contrib.admin.models import DELETION, LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.admin.utils import NestedObjects
from django.contrib.sessions.models import Session

from .utilities import flatten

admin.AdminSite.site_header = "Easy Wins With The Django Admin"
admin.AdminSite.index_title = "EWWTDA Dashboard"


class VerboseDeleteModelAdmin(admin.ModelAdmin):
    def log_deletion(self, request, object, object_repr):
        # if only using 1 database, set using=default
        nested_object = NestedObjects(using="default")
        nested_object.collect([object])
        nested_objects = nested_object.nested()

        objects_to_log = flatten(nested_objects)
        root_object_log = None

        for object_to_log in objects_to_log:
            deletion_log = LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=get_content_type_for_model(object_to_log).pk,
                object_id=object_to_log.pk,
                object_repr=repr(object_to_log),
                action_flag=DELETION,
                change_message=repr(object_to_log.__dict__),
            )
            root_object_log = root_object_log or deletion_log

        return root_object_log


@admin.register(LogEntry)
class LogEntryAdmin(VerboseDeleteModelAdmin):
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
class SessionAdmin(VerboseDeleteModelAdmin):
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
