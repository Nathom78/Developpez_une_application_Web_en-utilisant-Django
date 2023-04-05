# mvp/forms.py
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, RadioSelect, Textarea

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

class TicketForm(ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {'description': Textarea(attrs={"rows": "5"})}


class ReviewForm(ModelForm):
    
    class Meta:
        model = models.Review
        widgets = {
            'rating': RadioSelect(
                attrs={"class": "d-flex gap-4 ps-3"},
                choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]),
            'body': Textarea(attrs={"rows": "5"})
            
        }
        fields = ['headline', 'rating', 'body']
