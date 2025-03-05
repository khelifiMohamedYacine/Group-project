from django.shortcuts import render, redirect
from .models import UserAccount
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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
            messages.success(request, f'Welcome, {user.username}!')
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
    # For each task in task_data: [category, task, location, URL name]
    task_data = [
        ['Jumping Game', 'Complete Level 1', 'The Forum', 'jumping_game'],
        ['Quiz', 'Complete Quiz 1', 'The Forum', 'quizzes:quiz'],
        ['Jumping Game', 'Complete Level 2', 'The Forum', 'jumping_game'],
        ['Quiz', 'Complete Quiz 2', 'The Amory', 'quizzes:quiz'],
        ['Quiz', 'Complete Quiz 3', 'The Amory', 'quizzes:quiz'],
        ['Jumping Game', 'Complete Level 3', 'The Amory', 'jumping_game'],
        ['Quiz', 'Complete Quiz 4', 'Streatham Court', 'quizzes:quiz'],
    ]

    return render(request, 'core_app/home.html', {'user': request.user, 'task_data' : task_data})


def forgot_password_view(request):
    return render(request, 'core_app/forgot-password.html')


def privacy_policy_view(request):
    return render(request, 'core_app/privacy-policy.html')


def games_view(request):
    return render(request, 'core_app/games-page.html')


def maps_view(request):
    return render(request, 'core_app/maps.html')


def videos_view(request):
    return render(request, 'core_app/video.html')


def leaderboard_view(request):
    # This is also dummy data for now.
    leaderboard_data = [
        {'username' : 'Dummy User 3', 'reward_pts' : 75},
        {'username' : 'Dummy User 1', 'reward_pts' : 54},
        {'username' : 'Dummy User 4', 'reward_pts' : 54},
        {'username' : 'Dummy User 5', 'reward_pts' : 48},
        {'username' : 'Dummy User 2', 'reward_pts' : 39},
    ]

    return render(request, 'core_app/leaderboard.html', {'leaderboard_data' : leaderboard_data})


def admin_view(request):
    if request.user.is_authenticated:
        if request.user.account_type == "admin":
            # Allow the user to access the admin page if they are logged into an admin account
            return render(request, 'core_app/admin.html')
        else:
            # Return the user to the home page if they are logged in but not into an admin account
            return redirect('home')
    else:
        # Return the user to the login page if they are not logged in.
        return redirect('login')
    