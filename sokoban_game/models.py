from django.db import models
from core_app.models import UserAccount
import json

class sokoban_level(models.Model):
    number = models.IntegerField(unique=True)
    map_data = models.TextField()
    box_positions = models.TextField()
    person_position = models.TextField()

    def __str__(self):
        return f"Level {self.number}"

    def get_map(self):
        return json.loads(self.map_data)

    def get_box_positions(self):
        return json.loads(self.box_positions)

    def get_person_position(self):
        return json.loads(self.person_position)


# IDK if we're keeping this
class sokoban_results(models.Model):
    user_id = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
    )
    level_id = models.ForeignKey(
        sokoban_level,
        on_delete=models.CASCADE,
    )
    steps = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user_id.username} - Level {self.level_id.name} - {self.steps} steps"
