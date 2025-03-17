from django.db import models
from django.core.exceptions import ValidationError

class Location(models.Model):
    locID = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(default="Exeter")
    location_name = models.CharField(max_length=100, default="Location Name")  # User-defined name
    checked_in = models.BooleanField(default=False)

    locked_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    task1_id = models.CharField(null=True, blank=True, max_length=100)
    task2_id = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return f"{self.location_name}"
