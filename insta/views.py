from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from annoying.decorators import ajax_request

from insta.forms import CustomUserCreationForm
from insta.models import InstaUser, Post, UserConnection

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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UserProfile(DetailView):
    model = InstaUser
    template_name = 'user_profile.html'

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
