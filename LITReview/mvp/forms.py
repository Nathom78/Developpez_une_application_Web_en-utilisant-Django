# mvp/forms.py
from django.forms import ModelForm, RadioSelect, Textarea
from django.utils.translation import gettext_lazy as _

from . import models


class TicketForm(ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {'description': Textarea(attrs={"rows": "5"})}
        labels = {'title': _('Title')}


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
        labels = {
                'headline': _('Headline'),
                'body': _('Body'),
                'rating': _('Rating')
        }


class ReviewUpdateForm(ModelForm):

    class Meta:
        model = models.Review
        widgets = {
            'rating': RadioSelect(
                attrs={"class": "d-flex gap-4 ps-3"},
                choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
            ),
            'body': Textarea(attrs={"rows": "5"})

        }
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': _('Headline'),
            'body': _('Body'),
            'rating': _('Rating')
        }
