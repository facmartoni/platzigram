from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import redirect

# Permitir la visualización de imágenes en el admin 👇🏼

from django.conf import settings
from django.conf.urls.static import static

from platzigram import views as local_views
from posts import views as posts_views
from users import views as users_views

urlpatterns = [
    path('', local_views.home, name="home"),
    path('admin/', admin.site.urls, name="admin"),
    path('hello-world', local_views.hello_world, name="hello_world"),
    path('hi', local_views.sort_integers, name='hi'),
    path('person/<str:name>/<int:age>', local_views.person, name='person'),
    path('posts', posts_views.list_posts, name='feed'),
    path('posts/new', posts_views.create_post, name='create_post'),
    path('users/login', users_views.login_view, name='login'),
    path('users/logout', users_views.logout_view, name='logout'),
    path('users/signup', users_views.signup, name='signup'),
    path('users/me/profile', users_views.update_profile, name='update_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
