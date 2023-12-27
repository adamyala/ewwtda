from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    organization = models.ForeignKey(
        to="gatherdown.Organization", on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    image_url = models.URLField()

    def __str__(self):
        return self.name
