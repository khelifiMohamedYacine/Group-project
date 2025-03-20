from django.db import models
from django.core.exceptions import ValidationError
from core_app.models import UserAccount
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Location(models.Model):
    locID = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(default="Exeter")
    location_name = models.CharField(max_length=100, default="Location Name")  # User-defined name
    #checked_in = models.BooleanField(default=False)

    locked_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    # using GenericForeignKey allows a foreign key to multiple different task tables
    task1_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE, related_name='task1_type')
    task1_id = models.PositiveIntegerField(null=True, blank=True)
    task1 = GenericForeignKey('task1_type', 'task1_id')
    
    task2_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE, related_name='task2_type')
    task2_id = models.PositiveIntegerField(null=True, blank=True)
    task2 = GenericForeignKey('task2_type', 'task2_id')

    def __str__(self):
        return f"{self.location_name}"

class UserLocation(models.Model):
    userID = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    locationID = models.ForeignKey(Location, on_delete=models.CASCADE)
    checked_in = models.BooleanField(default=False)
    task1_complete = models.BooleanField(default=True)#default=True means that if no task is set the user doesnt need to complete it
    task2_complete = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.userID.username} - {self.locationID.locID}"

