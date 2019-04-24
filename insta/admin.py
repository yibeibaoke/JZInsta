from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from insta.models import Post, InstaUser
from insta.forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.
admin.site.register(Post)

class InstaUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'username', 'age']
    model = InstaUser

admin.site.register(InstaUser, InstaUserAdmin)