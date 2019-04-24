from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from insta.models import InstaUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = InstaUser
        fields = ('username', 'email', )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = InstaUser
        fields = ('username', 'email', )
