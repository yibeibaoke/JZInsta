from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from insta.forms import CustomUserCreationForm
from insta.models import InstaUser, Post

# Create your views here.

class IndexView(ListView):
    # model = Post.object.filter(title)
    model = Post
    template_name = 'index.html'


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class MakePost(CreateView):
    model = Post
    success_url = reverse_lazy('index')
    fields = ['title', 'image', ]
    template_name = 'make_post.html'