from django.shortcuts import render, redirect
from .models import UserAccount
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from core_app.models import UserAccount
from quizzes.models import Quiz, Question
from jumping_game.models import JumpingGameLevel

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, F
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

    games = []
    if request.user.is_authenticated:
        user_locations = UserLocation.objects.filter(userID=user)
    
        # populate the games data dynamically
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
    return render(request, 'core_app/home.html', {'user': request.user, 'games': games})



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
    return render(request, 'core_app/games-page.html', {'games': games})
    

def videos_view(request):
    return render(request, 'core_app/video.html')


def leaderboard_view(request):
    
    leaderboard_data = UserAccount.objects.order_by('-reward_pts').values('username', 'reward_pts')[:10]
    return render(request, 'core_app/leaderboard.html', {'leaderboard_data': leaderboard_data})

@login_required
def admin_view(request):
    """This is the view function for the Admin Dashboard page"""

    if request.user.is_authenticated:
        if request.user.account_type == "admin":
            # Allow the user to access the admin dashboard page if they are logged into an admin account
            return render(request, 'core_app/admin-dashboard.html')
        else:
            # Return the user to the home page if they are logged in but not into an admin account
            return redirect('home')
    else:
        # Return the user to the login page if they are not logged in.
        return redirect('login')


def admin_content_view(request):
    """This is the view function for the Content Management page"""

    if request.user.is_authenticated:
        if request.user.account_type == "admin":
            return render(request, 'core_app/manage-content.html')
        else:
            return redirect('home')
    else:
        return redirect('login')


def admin_users_view(request):
    """This is the view function for the Manage Users page"""

    if request.user.is_authenticated:
        if request.user.account_type == "admin":
            context = {
                'messageClass': "noResult",
                'message' : "",
                'userDetails' : []
            }

            if request.method == 'POST' and request.POST['whichForm'] == "userLookupForm":
                # This means the user lookup form was just submitted

                usem = request.POST['username-email']
                user = None

                if UserAccount.objects.filter(username = usem).exists():
                    user = UserAccount.objects.get(username = usem)
                elif UserAccount.objects.filter(email = usem).exists():
                    user = UserAccount.objects.get(email = usem)

                if user != None:
                    context["messageClass"] = "resultSuccess"
                    context["message"] = f"Successfully retrieved the details for the user '{user.username}'!"

                    context['userDetails'].append(f"Username: {user.username}")
                    context['userDetails'].append(f"Email: {user.email}")
                    context['userDetails'].append(f"Is Active: {user.is_active}")
                    context['userDetails'].append(f"Last Login: {user.last_login}")
                    context['userDetails'].append(f"Date Joined: {user.date_joined}")
                    context['userDetails'].append(f"Reward Points: {user.reward_pts}")
                    context['userDetails'].append(f"Account Type: {user.account_type}")
                    
                else:
                    context["messageClass"] = "resultFail"
                    context["message"] = f"""No account with the username or email address '{usem}' could be found.
                        Make sure your spelling is correct."""

            elif request.method == 'POST' and request.POST['whichForm'] == "adminPrivForm":
                # This means the user lookup form was just submitted
                
                if UserAccount.objects.filter(email = request.POST['email']).exists():
                    if request.POST['email'] == request.user.email:
                        # Do not allow an admin to demote the account they are currently using.
                        context["messageClass"] = "resultFail"
                        context["message"] = f"""You cannot change the type of your own account while you are using it.
                            Try asking another admin to do this for you."""

                    else:
                        user = UserAccount.objects.get(email = request.POST['email'])
                        user.account_type = request.POST['account-type']
                        user.save()

                        context["messageClass"] = "resultSuccess"
                        if user.account_type == "admin":
                            context["message"] = f"""The account '{user.username}' (email adrress: {user.email}) 
                                has successfully been changed to an admin account!"""
                        else:
                            context["message"] = f"""The account '{user.username}' (email adrress: {user.email}) 
                                has successfully been changed to a regular user account!"""
                    
                else:
                    context["messageClass"] = "resultFail"
                    context["message"] = f"""No account with the email address '{request.POST['email']}' could be found.
                        Make sure your spelling is correct."""

            elif request.method == 'POST' and request.POST['whichForm'] == "rewardPointsForm":
                # This means the user lookup form was just submitted
                
                usem = request.POST['username-email']
                user = None

                if UserAccount.objects.filter(username = usem).exists():
                    user = UserAccount.objects.get(username = usem)
                elif UserAccount.objects.filter(email = usem).exists():
                    user = UserAccount.objects.get(email = usem)

                try:
                    if user != None:
                        # The given user does exist
                        if request.POST['set-or-add'] == 'set':
                            if int(request.POST['reward_pts']) < 0:
                                context["messageClass"] = "resultFail"
                                context["message"] = f"""A user's total number of reward points cannot be less than zero."""
                            else:
                                user.reward_pts = int(request.POST['reward_pts'])
                                user.save()
                                context["messageClass"] = "resultSuccess"
                                context["message"] = f"""The user '{user.username}' now has {user.reward_pts} reward points."""

                        elif request.POST['set-or-add'] == 'add':
                            if user.reward_pts + int(request.POST['reward_pts']) < 0:
                                context["messageClass"] = "resultFail"
                                context["message"] = f"""A user's total number of reward points cannot be less than zero."""
                            else:
                                user.reward_pts = F("reward_pts") + request.POST['reward_pts']
                                user.save()
                                user.refresh_from_db()
                                context["messageClass"] = "resultSuccess"
                                context["message"] = f"""The user '{user.username}' now has {user.reward_pts} reward points."""
                    else:
                        # The given user does not exist
                        context["messageClass"] = "resultFail"
                        context["message"] = f"""No account with the username or email address '{usem}' could be found.
                            Make sure your spelling is correct."""

                except ValueError:
                    # This could only happen if the form was posted illegitimately (not through the website)
                    context["messageClass"] = "resultFail"
                    context["message"] = f"""An unknown error occurred."""

            return render(request, 'core_app/manage-users.html', context)
        else:
            return redirect('home')
    else:
        return redirect('login')


def admin_analytics_view(request):
    """This is the view function for the Website Analytics page"""

    if request.user.is_authenticated:
        if request.user.account_type == "admin":
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

            return render(request, 'core_app/analytics.html', context)
        else:
            return redirect('home')
    else:
        return redirect('login')


def admin_quiz_view(request):
    """This is the view function for the Manage Quizzes page"""

    if request.user.is_authenticated:
        if request.user.account_type == "admin":
            context = {
                'messageClass': "noResult",
                'message' : "",
                'currentQuizzes' : []
            }

            if request.method == 'POST' and request.POST['whichForm'] == "addQuizForm":
                # This means the add quiz form was just submitted

                if Quiz.objects.filter(name = request.POST['quiz-name']).exists():
                    # The new quiz is not allowed to have the same name as an existing one
                    context["messageClass"] = "resultFail"
                    context["message"] = f"There is already a quiz with the name '{request.POST['quiz-name']}'."

                elif not (request.POST['numberOfQuestions'].isnumeric()):
                    # This could only happen if the form was posted illegitimately (not through the website)
                    context["messageClass"] = "resultFail"
                    context["message"] = f"An unknown error occurred."

                else:
                    noOfQuestions = int(request.POST['numberOfQuestions'])
                    duplicateQuestionFound = False

                    for x in range(1, noOfQuestions + 1):
                        # Check questions against the database for duplicates
                        if Question.objects.filter(question_text = request.POST['question-text-q' + str(x)]).exists():
                            # No duplicates of existing questions are allowed
                            duplicateQuestionFound = True
                            context["messageClass"] = "resultFail"
                            context["message"] = f"""The question '{request.POST['question-text-q' + str(x)]}' 
                                is already in another quiz. Try re-wording the question slightly."""
                            break

                    if noOfQuestions > 1:
                        for x in range(1, noOfQuestions):
                            for y in range(x + 1, noOfQuestions + 1):
                                # Check questions against each other for duplicates
                                if request.POST['question-text-q' + str(x)] == request.POST['question-text-q' + str(y)]:
                                    # No duplicates of existing questions are allowed
                                    duplicateQuestionFound = True
                                    context["messageClass"] = "resultFail"
                                    context["message"] = f"""The question '{request.POST['question-text-q' + str(x)]}' 
                                        appears multiple times in this quiz."""
                                    break

                    if duplicateQuestionFound == False:
                        # If all validation checks have passed, then add the quiz and questions to the database
                        context["messageClass"] = "resultSuccess"
                        context["message"] = "The new quiz was successfully added!"

                        newQuiz = Quiz(name = request.POST['quiz-name'])
                        newQuiz.save()

                        for x in range(1, noOfQuestions + 1):
                            correct = request.POST['correct-choice-q' + str(x)]
                            newQuestion = Question(
                                question_text = request.POST['question-text-q' + str(x)],
                                choice1 = request.POST['choice1-q' + str(x)],
                                choice2 = request.POST['choice2-q' + str(x)],
                                choice3 = request.POST['choice3-q' + str(x)],
                                choice4 = request.POST['choice4-q' + str(x)],
                                correct_choice = request.POST['choice' + correct + '-q' + str(x)],
                                quiz = newQuiz
                            )
                            newQuestion.save()
                        
            elif request.method == 'POST' and request.POST['whichForm'] == "deleteQuizForm":
                # This means the delete quiz form was just submitted

                if Quiz.objects.filter(name = request.POST['select-quiz']).exists():
                    # Confirm that a quiz with the given name exists within the database
                    Quiz.objects.filter(name = request.POST['select-quiz']).delete()
                    context["messageClass"] = "resultSuccess"
                    context["message"] = f"The quiz '{request.POST['select-quiz']}' was successfully deleted!"
                
                else:
                    context["messageClass"] = "resultFail"
                    context["message"] = f"""No quiz named '{request.POST['select-quiz']}' could be found.
                        This is likely because it was recently deleted."""

            context["currentQuizzes"] = list(Quiz.objects.values_list('name', flat=True))
            return render(request, 'core_app/manage-quiz.html', context)
        else:
            return redirect('home')
    else:
        return redirect('login')
    

def admin_jumping_view(request):
    """This is the view function for the Manage Jumping Game page"""

    if request.user.is_authenticated:
        if request.user.account_type == "admin":
            context = {
                'messageClass': "noResult",
                'message' : "",
                'levelIDs' : []
            }

            if request.method == 'POST' and request.POST['whichForm'] == "addLevelForm":
                # This means the add level form was just submitted

                sm = request.POST['speed-multi']
                sp = request.POST['spawn-rate']

                if sm.replace('.','',1).isdigit() == True and sp.isnumeric():
                    # Only add a new level if the values given can be converted into the correct type

                    context["messageClass"] = "resultSuccess"
                    context["message"] = f"The level was successfully added!"

                    newLevel = JumpingGameLevel(
                        speed_multiplier = float(sm),
                        enemy_spawn_rate = int(sp)
                    )
                    newLevel.save()

                else:
                    # This could only happen if the form was posted illegitimately (not through the website)
                    context["messageClass"] = "resultFail"
                    context["message"] = f"An unknown error occurred."

            elif request.method == 'POST' and request.POST['whichForm'] == "editLevelForm":
                # This means the edit level form was just submitted

                if not (request.POST['select-level'].isnumeric()):
                    # This could only happen if the form was posted illegitimately (not through the website)
                    context["messageClass"] = "resultFail"
                    context["message"] = f"An unknown error occurred."

                elif JumpingGameLevel.objects.filter(id = int(request.POST['select-level'])).exists():
                    # Confirm that a level with the given ID exists in the Jumping game database

                    sm = request.POST['speed-multi']
                    sp = request.POST['spawn-rate']

                    if sm.replace('.','',1).isdigit() == True and sp.isnumeric():
                        # Only add a new level if the values given can be converted into the correct type

                        context["messageClass"] = "resultSuccess"
                        context["message"] = f"The level was successfully edited!"

                        editLevel = JumpingGameLevel.objects.get(id = int(request.POST['select-level']))
                        editLevel.speed_multiplier = float(sm)
                        editLevel.enemy_spawn_rate = int(sp)
                        editLevel.save()

                    else:
                        # This could only happen if the form was posted illegitimately (not through the website)
                        context["messageClass"] = "resultFail"
                        context["message"] = f"An unknown error occurred."

                else:
                    context["messageClass"] = "resultFail"
                    context["message"] = f"""No level with an ID of '{request.POST['select-level']}' could be found. 
                        This is likely because it was recently deleted."""                  

            elif request.method == 'POST' and request.POST['whichForm'] == "deleteLevelForm":
                # This means the delete level form was just submitted

                if not (request.POST['select-level'].isnumeric()):
                    # This could only happen if the form was posted illegitimately (not through the website)
                    context["messageClass"] = "resultFail"
                    context["message"] = f"An unknown error occurred."

                elif JumpingGameLevel.objects.filter(id = int(request.POST['select-level'])).exists():
                    # Confirm that a level with the given ID exists in the Jumping game database
                    JumpingGameLevel.objects.filter(id = int(request.POST['select-level'])).delete()
                    context["messageClass"] = "resultSuccess"
                    context["message"] = f"The level with an ID of '{request.POST['select-level']}' was successfully deleted!"
                
                else:
                    context["messageClass"] = "resultFail"
                    context["message"] = f"""No level with an ID of '{request.POST['select-level']}' could be found. 
                        This is likely because it was recently deleted.""" 

            context["levelIDs"] = list(JumpingGameLevel.objects.values_list('id', flat=True))
            return render(request, 'core_app/manage-jumping.html', context)
        else:
            return redirect('home')
    else:
        return redirect('login')
