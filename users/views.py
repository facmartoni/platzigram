"""User views"""
from django.shortcuts import render, redirect
from django.views.generic import DetailView, FormView, UpdateView
from django.urls import reverse_lazy, reverse

# Login imports 👇🏼

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views

# Models
from django.contrib.auth.models import User
from users.models import Profile
from posts.models import Post

# Exceptions
from django.core.exceptions import ObjectDoesNotExist

# Forms
from users.forms import LoginForm, SignupForm


class LoginView(auth_views.LoginView):
    """Login view"""
    template_name = 'users/login.html'


# def login_view(request):
#     """Login view"""
#     # import pdb
#     # pdb.set_trace()
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         username = request.POST['username']
#         password = request.POST['password']

#         # usernames = [user.username for user in User.objects.all()]

#         try:
#             User.objects.get(username=username)
#         except ObjectDoesNotExist:
#             return render(request, 'users/login.html', {
#                 'error': 'This username does not exist',
#                 'username_error': True,
#                 'form': form
#             })

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         if user:
#             login(request, user)
#             return redirect('posts:feed')
#         else:
#             return render(request, 'users/login.html', {
#                 'error': 'Invalid password',
#                 'password_error': True,
#                 'form': form
#             })
#     else:
#         form = LoginForm()
#         return render(request, 'users/login.html', {
#             'form': form
#         })


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view"""

    pass

# @login_required
# def logout_view(request):
#     """Logout a user"""

#     logout(request)
#     return redirect('users:login')


class SignupView(FormView):
    """Users sign up view"""

    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('posts:feed')

    def form_valid(self, form):
        """Save form data"""
        form.save()

        self.username = form.cleaned_data['username']
        self.password = form.cleaned_data['password']

        user = authenticate(
            self.request,
            username=self.username,
            password=self.password
        )

        if user:
            login(self.request, user)

        return super().form_valid(form)


# def signup(request):
#     """Signup view"""

#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('posts:feed')
#     else:
#         form = SignupForm()
#     return render(
#         request,
#         'users/signup.html',
#         {
#             'form': form,
#         }
#     )


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view"""

    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']
    template_name = 'users/update_profile.html'

    def get_object(self):
        """Return user's profile"""

        return self.request.user.profile

    def get_success_url(self):
        """Return to user's profile"""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})


# @login_required
# def update_profile(request):
#     """Update a profile view"""

#     profile = request.user.profile

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             data = form.cleaned_data
#             profile.website = data['website']
#             profile.phone_number = data['phone_number']
#             profile.biography = data['biography']
#             if data['picture']:
#                 profile.picture = data['picture']
#             profile.save()
#             redirect('users:update')
#     else:
#         form = ProfileForm()

#     return render(
#         request,
#         'users/update_profile.html',
#         {
#             'profile': profile,
#             'user': request.user,
#             'form': form
#         }
#     )


class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail view"""

    queryset = User.objects.all()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's post to context."""

        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context
