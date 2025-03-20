from django.db import models

class jumping_game_level(models.Model):
    speed_multiplier = models.FloatField(default=2.0)
    enemy_spawn_rate = models.IntegerField(default=800)  # milliseconds
    #IDK const imageCycles = [1, 2, 2, 1];

    #def get_map(self):
    #    return json.loads(self.map_data)

    #def get_box_positions(self):
    #    return json.loads(self.box_positions)

    #def get_person_position(self):
    #    return json.loads(self.person_position)