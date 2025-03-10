from django.db import models
from core_app.models import UserAccount


class Level(models.Model):
    # just a stub figure this out later

    def __str__(self):
        return self.name

class sokoban_results(models.Model):
    user_id = models.CharField(max_length=100)
    level = models.IntegerField()
    steps = models.IntegerField()
    score = models.IntegerField() # is this not just a function of steps? Probably remove it

class SokobanResults(models.Model):
    user_id = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
    )
    level_id = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
    )
    steps = models.IntegerField(default=0)  # Default value for steps is 0

    def __str__(self):
        return f"{self.user_id.username} - Level {self.level_id.name} - {self.steps} steps"