from django.shortcuts import render, redirect
from .models import UserAccount
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        usernameOrEmail = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=usernameOrEmail, password=password) # allow email authentication as well
        if user:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):

    if request.method == 'POST': #user clicked the Sign Up button
        username = request.POST['username']# this is an issue with the html form and not my code
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        email = request.POST['email']

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
    return render(request, 'core_app/home-page.html', {'user': request.user})