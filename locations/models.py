from django.db import models
from django.core.exceptions import ValidationError

class Location(models.Model):
    locID = models.AutoField(primary_key=True, default=None)
    postcode = models.CharField(null=True, max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(default="Exeter")
    location_name = models.CharField(max_length=100, default="Location Name")  # User-defined name
    locked_by = models.IntegerField(null=True, blank=True)
    checked_in = models.BooleanField(default=False)

    task1_id = models.CharField(null=True, blank=True, max_length=100)
    task2_id = models.CharField(null=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        # Convert postcode to uppercase
        self.postcode = self.postcode.upper()
        
        # Check if locked_by refers to an existing Location ID
        if self.locked_by is not None:
            if not Location.objects.filter(locID=self.locked_by).exists():
                raise ValidationError(f"Parent location with ID {self.locked_by} does not exist.")
        super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.location_name}"
