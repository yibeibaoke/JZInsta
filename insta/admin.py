from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from insta.models import Post, InstaUser, UserConnection
from insta.forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.

class InstaUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'username', 'age',]
    model = InstaUser

admin.site.register(Post)
admin.site.register(InstaUser, InstaUserAdmin)
admin.site.register(UserConnection)
