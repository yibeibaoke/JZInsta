from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from insta.models import Post, InstaUser, UserConnection, Comment, Like
from insta.forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.

class InstaUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'username', 'age',]
    model = InstaUser

class CommentInline(admin.StackedInline):
    model = Comment

class LikeInline(admin.StackedInline):
    model = Like

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
        LikeInline,
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(InstaUser, InstaUserAdmin)
admin.site.register(UserConnection)
admin.site.register(Comment)
admin.site.register(Like)
