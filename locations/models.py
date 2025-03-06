from django.db import models

class Location(models.Model):
    locID = models.AutoField(primary_key=True, default=None)
    postcode = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(default="Exeter")  # Stores the full address
    location_name = models.CharField(max_length=100, default="Location Name")  # User-defined name

    task1_id = models.IntegerField(null=True, blank=True)
    task2_id = models.IntegerField(null=True, blank=True)
    task3_id = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.postcode = self.postcode.upper()  # Convert postcode to uppercase
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.location_name}"
