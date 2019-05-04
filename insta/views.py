from annoying.decorators import ajax_request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from insta.forms import CustomUserCreationForm
from insta.models import (Comment, InstaPost, InstaUser, Like, Post,
                          UserConnection)

# Create your views here.

class IndexView(LoginRequiredMixin, ListView):
    model = InstaPost
    template_name = 'index.html'
    login_url = 'login'

    def get_queryset(self):
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return InstaPost.objects.filter(author__in=following)

class ExploreView(LoginRequiredMixin, ListView):
    model = InstaPost
    template_name = 'explore.html'
    login_url = 'login'

    def get_queryset(self):
        return InstaPost.objects.all().order_by('-posted_on')[:20]

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class MakeInstaPost(LoginRequiredMixin, CreateView):
    model = InstaPost
    success_url = reverse_lazy('index')
    fields = ['title', 'image',]
    template_name = 'make_post.html'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class MakePost(LoginRequiredMixin, CreateView):
    model = Post
    success_url = reverse_lazy('index')
    fields = ['title', 'image', ]
    template_name = 'make_post.html'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetail(LoginRequiredMixin, DetailView):
    model = InstaPost
    template_name = 'post_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        liked = Like.objects.filter(post=self.kwargs.get('pk'), user=self.request.user).first()
        if liked:
            data['liked'] = 1
        else:
            data['liked'] = 0
        return data

class UserProfile(LoginRequiredMixin, DetailView):
    model = InstaUser
    template_name = 'user_profile.html'
    login_url = 'login'

class EditProfile(LoginRequiredMixin, UpdateView):
    model = InstaUser
    template_name = 'edit_profile.html'
    fields = ['profile_pic', 'username']
    login_url = 'login'

class FollowerProfile(LoginRequiredMixin, ListView):
    model = InstaUser
    template_name = 'connections.html'
    login_url = 'login'

    def get_queryset(self):
        user_pk = self.kwargs['pk']
        this_user = InstaUser.objects.filter(pk=user_pk)
        followers = set()
        for conn in UserConnection.objects.filter(following__in=this_user):
            followers.add(conn.creator.pk)
        return InstaUser.objects.filter(pk__in=followers)

class FollowingProfile(LoginRequiredMixin, ListView):
    model = InstaUser
    template_name = 'connections.html'
    login_url = 'login'

    def get_queryset(self):
        following = set()
        connection_set = UserConnection.objects.filter(creator__pk=self.kwargs['pk'])

        for connection in connection_set:
            following.add(connection.following.pk)
        return InstaUser.objects.filter(pk__in=following)

@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }

@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = InstaPost.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }


@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = InstaPost.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }
