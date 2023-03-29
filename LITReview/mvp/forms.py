# mvp/forms.py
from django.utils.translation import gettext_lazy as _
from django import forms

from . import models


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
