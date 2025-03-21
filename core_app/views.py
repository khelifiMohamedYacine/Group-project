from django.shortcuts import render, redirect
from .models import UserAccount
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from core_app.models import UserAccount


def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']

        # try authenticating with username
        user = authenticate(request, username=username_or_email, password=password)

        # if that fails use the input as email and try to find the user
        # note this implementation has a potencial bug if another user1 has username same as user2's email
        # need to decide what to do about it
        if not user:
            try:
                # try to find the user by email
                user_object = UserAccount.objects.get(email=username_or_email)

                user = authenticate(request, username=user_object.username, password=password)
            except UserAccount.DoesNotExist:
                user = None


        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username, email or password')

    return render(request, 'core_app/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):

    if request.method == 'POST': #user clicked the Sign Up button
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        email = request.POST['email']

        # check if details entered are valid
        if '@' in username:
            messages.error(request, 'Usernames cannot contain @ character')
            return redirect('register')
        if '@' not in email:
            messages.error(request, 'Valid emails must contain @ character')
            return redirect('register')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        if UserAccount.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('register')
        if UserAccount.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')
            return redirect('register')

        # create a user account
        user = UserAccount(
            username=username,
            email=email,
        )
        user.set_password(password) # this does the hashing for us
        user.save()

        return redirect('login')

    return render(request, 'core_app/create-account.html')


def home_view(request):

    # This is dummy data for now.
    # For each task in task_data: [icons, category, task, location, URL name]
    task_data = [
        ['fas fa-angle-double-up', 'Jumping Game', 'Complete Level 1', 'The Forum', 'jumping_game'],
        ['fas fa-question', 'Quiz', 'Complete Quiz 1', 'The Forum', 'quizzes:quiz'],
        ['fas fa-angle-double-up', 'Jumping Game', 'Complete Level 2', 'The Forum', 'jumping_game'],
        ['fas fa-question', 'Quiz', 'Complete Quiz 2', 'The Amory', 'quizzes:quiz'],
        ['fas fa-question', 'Quiz', 'Complete Quiz 3', 'The Amory', 'quizzes:quiz'],
        ['fas fa-angle-double-up', 'Jumping Game', 'Complete Level 3', 'The Amory', 'jumping_game'],
        ['fas fa-question', 'Quiz', 'Complete Quiz 4', 'Streatham Court', 'quizzes:quiz'],
    ]
    # Get icons from: https://www.w3schools.com/icons/icons_reference.asp

    return render(request, 'core_app/home.html', {'user': request.user, 'task_data' : task_data})


def forgot_password_view(request):
    return render(request, 'core_app/forgot-password.html')


def privacy_policy_view(request):
    return render(request, 'core_app/privacy-policy.html')

from locations.models import Location, UserLocation

@login_required
def games_view(request):

    # store of data that doesnt change
    game_info = { 
        'quiz': {
            'url': "quizzes:quiz",
            'image': 'cc.png',
            'description': 'Test your knowledge in the quiz game.'
        },
        'sokoban_level': {
            'url': 'sokoban_game',
            'image': 'SokobanGamePic1.PNG',
            'description': 'Help Mark recycle the garbage in this puzzle game.'
        },
        'jumping game level': { # well that did fix the bug
            'url': 'jumping_game',
            'image': 'JumpingGamePic2.PNG',
            'description': 'Lead the dog to a cleaner environment by jumping and rolling around obstacles.'
        }
    }
    user = request.user
    locations = Location.objects.all()
    user_locations = UserLocation.objects.filter(userID=user)
    
    # populates the games data dynamically
    games = []
    for location in locations:

        user_location = user_locations.filter(locationID=location).first()

        if user_location is None or not user_location.checked_in:
            continue

        if not user_location.task1_complete:
            task1_type = location.task1_type.name if location.task1_type else None
            game_data = game_info[task1_type]
            game_id = location.task1_id

            game = {
                "name": location.location_name,
                "location_name": location.location_name,
                "description": game_data['description'],
                "image": game_data['image'],
                "game_url": game_data['url'],
                "game_id": game_id,
            }
            games.append(game)

        if not user_location.task2_complete:
            task2_type = location.task2_type.name if location.task2_type else None
            game_data = game_info[task2_type]
            game_id = location.task2_id

            game = {
                "name": location.location_name,
                "location_name": location.location_name,
                "description": game_data['description'],
                "image": game_data['image'],
                "game_url": game_data['url'],
                "game_id": game_id,
            }
            games.append(game)
    print("sent games data", games)
    
    return render(request, 'core_app/games-page.html', {'games': games})
    

def videos_view(request):
    return render(request, 'core_app/video.html')


def leaderboard_view(request):
    
    leaderboard_data = UserAccount.objects.order_by('-reward_pts').values('username', 'reward_pts')[:10]
    return render(request, 'core_app/leaderboard.html', {'leaderboard_data': leaderboard_data})

@login_required
def admin_view(request):

    if request.user.account_type == "admin":
        return render(request, 'core_app/admin-dashboard.html')
    else:
        # send the user to the home page if they are logged in but not into a game_admin account
        return redirect('home')
    