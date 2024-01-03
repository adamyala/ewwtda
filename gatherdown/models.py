import csv
from io import StringIO

from django.contrib.auth import get_user_model
from django.db import models
from django.template.loader import render_to_string


class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    organization = models.ForeignKey(
        to="gatherdown.Organization", on_delete=models.CASCADE,
    )
    attendees = models.ManyToManyField(
        to=get_user_model(), blank=True,
    )
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    image_url = models.URLField()

    def __str__(self):
        return self.name

    def file_download(self):
        file_content = self.file_download_content()
        context = {
            "file_name": "attendees.csv",
            "file_content": file_content,
            "file_content_type": "text/csv",
        }
        html = render_to_string("file-download.html", context)
        return html

    def file_download_content(self):
        buffer = StringIO()
        csv_writer = csv.writer(buffer)

        headers = ["username", "email"]
        csv_writer.writerow(headers)

        attendees = self.attendees.values_list(*headers)
        for row in attendees:
            csv_writer.writerow(row)

        content = buffer.getvalue()

        return content
