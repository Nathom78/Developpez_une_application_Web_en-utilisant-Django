# mvp/forms.py
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms

from . import models

User = get_user_model()


# class FollowUsersForm(forms.ModelForm):
#     class Meta:
#         model = models.UserFollows
#         fields = ['user', 'followed_user']
#
#
# class UsersForm(forms.ModelForm):
#     user_searching = forms.BooleanField(widget=forms.HiddenInput, initial=True)
#
#     class Meta:
#         model = User
#         fields = ['username']