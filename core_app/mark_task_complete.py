from django.contrib.contenttypes.models import ContentType

from quizzes.models import Quiz
from .models import UserAccount
from locations.models import UserLocation, Location
from sokoban_game.models import sokoban_level

def mark_task_complete(user, task_type_string, task_id, reward_pts):
    if not user.is_authenticated:
        raise PermissionDenied("User must be logged in")
        return


    task_type = None
    match task_type_string:
        case "Quiz":
            task_type = ContentType.objects.get_for_model(Quiz)
        case "JumpingGameLevel":
            task_type = ContentType.objects.get_for_model(JumpingGameLevel)
        case "sokoban_level":
            task_type = ContentType.objects.get_for_model(sokoban_level)

    user_locations = UserLocation.objects.filter(userID=user, checked_in=True)  # Filter for checked-in locations
    # check through every UserLocation the user has check in to
    for user_location in user_locations:
        # Get the associated Location object
        location = user_location.locationID

        # Check if task1 matches the task_id
        if location.task1_id == task_id and location.task1_type == task_type:
            user_location.task1_complete = True
            print(f"Updated task completion for user {user.username} at location {location.location_name}, task1")
        
        # Check if task2 matches the task_id
        if location.task2_id == task_id and location.task2_type == task_type:
            user_location.task2_complete = True
            print(f"Updated task completion for user {user.username} at location {location.location_name}, task2")

        user_location.save()
    
    # give users their reward_pts
    #user_account = user.UserAccount
    user.reward_pts += reward_pts
    user.save()