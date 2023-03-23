from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from itertools import chain
from django.db.models import CharField, Value
from django.contrib.auth.decorators import login_required

from .forms import FollowUsersForm, UsersForm


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    
    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    
    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'feed.html', context={'posts': posts})


@login_required
class FollowUsers(View):
    
    print_form = FollowUsersForm
    input_form = UsersForm
    template_name = 'follow_users_forms.html'
    
    context = {
        'input_form': input_form,
        'print_form': print_form
    }
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, context=self.context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return
        
        return render(request, self.template_name, context=self.context)


# class MyFormView(View):
#     form_class = MyForm
#     initial = {'key': 'value'}
#     template_name = 'form_template.html'
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return HttpResponseRedirect('/success/')
#
#         return render(request, self.template_name, {'form': form})
