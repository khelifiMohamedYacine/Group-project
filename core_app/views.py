from django.shortcuts import render, redirect
from .models import UserAccount
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.db.models import Count
from core_app.models import UserAccount

from django.utils import timezone
from datetime import timedelta

from django.db.models.functions import TruncDate
import json


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


def games_view(request):
    return render(request, 'core_app/games-page.html')


def maps_view(request):
    return render(request, 'core_app/maps.html')


def videos_view(request):
    return render(request, 'core_app/video.html')


def leaderboard_view(request):
    
    leaderboard_data = UserAccount.objects.order_by('-reward_pts').values('username', 'reward_pts')[:10]
    return render(request, 'core_app/leaderboard.html', {'leaderboard_data': leaderboard_data})

def manage_users(request):
    return render(request, 'core_app/manage_users.html')

def content_manage(request):
    return render(request, 'core_app/content_manage.html')

def admin_view(request):
    if request.user.is_authenticated:
        if request.user.account_type == "admin":
            # Allow the user to access the admin dashboard page if they are logged into an admin account
            return render(request, 'core_app/admin_dashboard.html')
        else:
            # Return the user to the home page if they are logged in but not into an admin account
            return redirect('home')
    else:
        # Return the user to the login page if they are not logged in.
        return redirect('login')
    


from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import UserAccount
from django.db.models import Count
from django.db.models.functions import TruncDate
import json

def analyse_users(request):
    # Define the time frame for "recently active" (last 30 days)
    n_days = 30
    cutoff_date = timezone.now() - timedelta(days=n_days)

    # Count active and inactive users
    active_users = UserAccount.objects.filter(last_login__gte=cutoff_date).count()
    inactive_users = UserAccount.objects.filter(last_login__lt=cutoff_date).count()

    # User growth over time using TruncDate instead of extra()
    user_growth = (
        UserAccount.objects
        .annotate(date_joined_trunc=TruncDate('date_joined'))
        .values('date_joined_trunc')
        .annotate(count=Count('id'))
        .order_by('date_joined_trunc')
    )

    # Extracting dates and counts
    dates = [entry['date_joined_trunc'].strftime('%Y-%m-%d') for entry in user_growth]
    counts = [entry['count'] for entry in user_growth]

    # Pass data safely as JSON
    context = {
        'active_users': active_users,
        'inactive_users': inactive_users,
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'core_app/analysis.html', context)
