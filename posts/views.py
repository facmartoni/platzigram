"""Posts views"""

from django.shortcuts import render, redirect

# Login required imports 👇🏼
from django.contrib.auth.decorators import login_required

# Models
from posts.models import Post

# Forms
from posts.forms import PostForm


@login_required
def list_posts(request):
    """List existing posts"""

    posts = Post.objects.all().order_by('-created')
    return render(request, 'posts/feed.html', {
        'posts': posts
    })


@login_required
def create_post(request):
    """Create new post view"""
    if request.method == 'POST':
        form = PostForm({'title': request.POST['title'], 'user': request.user.pk,
                         'profile': request.user.profile.pk}, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(
        request,
        'posts/new.html',
        {
            'user': request.user,
            'form': form,
            'profile': request.user.profile,
        }
    )
