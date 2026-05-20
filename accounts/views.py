from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm


def register_view(request):
    """Handles new user registration."""
    if request.user.is_authenticated:
        return redirect('resume:form')  # Already logged in? Go to form.

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()                   # Save user to database
            login(request, user)                 # Log them in automatically
            messages.success(request, f'Welcome, {user.username}! Your account was created.')
            return redirect('resume:form')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Handles user login."""
    if request.user.is_authenticated:
        return redirect('resume:form')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('resume:form')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Logs out the user and redirects home."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')