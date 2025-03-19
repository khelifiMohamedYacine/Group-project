from django.db import models
from django.core.exceptions import ValidationError
from core_app.models import UserAccount
from quizzes.models import Quiz

class Location(models.Model):
    locID = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(default="Exeter")
    location_name = models.CharField(max_length=100, default="Location Name")  # User-defined name
    #checked_in = models.BooleanField(default=False)

    locked_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    task1 = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True, related_name="task1")
    task2 = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True, related_name="task2")

    def __str__(self):
        return f"{self.location_name} (ID: {self.locID})"

class UserLocation(models.Model):
    userID = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    locationID = models.ForeignKey(Location, on_delete=models.CASCADE)
    checked_in = models.BooleanField(default=False)
    task1_complete = models.BooleanField(default=False)
    task2_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.location.locID}"

