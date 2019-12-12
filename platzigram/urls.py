# Django
from django.contrib import admin
from django.urls import path, include

# Permitir la visualización de imágenes en el admin 👇🏼
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', include(('posts.urls', 'posts'), namespace='posts')),
    path('users/', include(('users.urls', 'users'), namespace='users')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
