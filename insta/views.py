from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from insta.forms import CustomUserCreationForm

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'