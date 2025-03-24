import os
import sys
import django
import json

# Calculate the root directory path of the Django project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the Django project root directory to sys.path
sys.path.append(BASE_DIR)

# Set up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sustainability_project.settings")

django.setup()

from sokoban_game.models import sokoban_level  # Ensure the model is correctly imported

LEVEL_JSON_PATH = None
if os.path.exists(os.path.join(BASE_DIR, "sokoban_game/static/sokoban_game/levels_admin.json")):
    LEVEL_JSON_PATH = os.path.join(BASE_DIR, "sokoban_game/static/sokoban_game/levels_admin.json")
else:
    print("error couldnt find path")
    quit()

# If no file is found, print an error message and exit
if LEVEL_JSON_PATH is None:
    print("ERROR: levels_admin.json file not found! Please check if the static directory contains the file.")
    sys.exit(1)

print(f"Reading JSON file: {LEVEL_JSON_PATH}")

# Read the JSON file and store the data in the database
with open(LEVEL_JSON_PATH, 'r', encoding='utf-8') as file:
    levels_data = json.load(file)

# Clear old data before importing new levels
sokoban_level.objects.all().delete()

for index, level in enumerate(levels_data):
    sokoban_level.objects.create(
        id=index + 1,
        map_data=json.dumps(level["map"]),
        box_positions=json.dumps(level["boxPos"]),
        person_position=json.dumps(level["personPos"])
    )

print("Level data has been successfully imported into the database!")