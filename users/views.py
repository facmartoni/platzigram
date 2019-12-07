"""User views"""
from django.shortcuts import render, redirect

# Login imports 👇🏼

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Models
from django.contrib.auth.models import User
from users.models import Profile

# Exceptions
from django.core.exceptions import ObjectDoesNotExist

# Forms
from users.forms import ProfileForm, LoginForm, SignupForm


def login_view(request):
    """Login view"""
    # import pdb
    # pdb.set_trace()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        # usernames = [user.username for user in User.objects.all()]

        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return render(request, 'users/login.html', {
                'error': 'This username does not exist',
                'username_error': True,
                'form': form
            })

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('feed')
        else:
            return render(request, 'users/login.html', {
                'error': 'Invalid password',
                'password_error': True,
                'form': form
            })
    else:
        form = LoginForm()
        return render(request, 'users/login.html', {
            'form': form
        })


@login_required
def logout_view(request):
    """Logout a user"""

    logout(request)
    return redirect('login')


def signup(request):
    """Signup view"""

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignupForm()
    return render(
        request,
        'users/signup.html',
        {
            'form': form,
        }
    )


@login_required
def update_profile(request):
    """Update a profile view"""

    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            if data['picture']:
                profile.picture = data['picture']
            profile.save()
            redirect('update_profile')
    else:
        form = ProfileForm()

    return render(
        request,
        'users/update_profile.html',
        {
            'profile': profile,
            'user': request.user,
            'form': form
        }
    )
