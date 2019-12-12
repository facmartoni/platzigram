"""Posts views"""

# Django
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

# Login required imports 👇🏼
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
from posts.models import Post

# Forms
from posts.forms import PostForm


class PostsFeedView(LoginRequiredMixin, ListView):
    """Return all published posts"""

    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 30
    context_object_name = 'posts'


class PostDetailView(LoginRequiredMixin, DetailView):
    """Post Detail View"""

    queryset = Post.objects.all()
    template_name = 'posts/detail.html'
    context_object_name = 'post'


class CreatePostView(LoginRequiredMixin, CreateView):
    """Create a new post"""

    model = Post
    template_name = 'posts/new.html'
    fields = ['title', 'photo']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.profile = self.request.user.profile
        form.save()
        return super(CreatePostView, self).form_valid(form)

    def get_success_url(self):
        return reverse('posts:feed')


# @login_required
# def create_post(request):
#     """Create new post view"""
#     if request.method == 'POST':
#         form = PostForm({'title': request.POST['title'], 'user': request.user.pk,
#                          'profile': request.user.profile.pk}, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('posts:feed')
#     else:
#         form = PostForm()
#     return render(
#         request,
#         'posts/new.html',
#         {
#             'user': request.user,
#             'form': form,
#             'profile': request.user.profile,
#         }
#     )
