from django.db import models

class JumpingGameLevel(models.Model):
    speed_multiplier = models.FloatField(default=2.0)
    enemy_spawn_rate = models.IntegerField(default=800)  # milliseconds

    #IDK const imageCycles = [1, 2, 2, 1];