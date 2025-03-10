from django.db import models

class game_record(models.Model):
    user_id = models.CharField(max_length=100)
    level = models.IntegerField()
    steps = models.IntegerField()
    score = models.IntegerField()
