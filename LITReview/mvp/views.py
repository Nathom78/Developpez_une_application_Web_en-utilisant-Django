from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from itertools import chain
from django.db.models import CharField, Value
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import UserFollows


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


# @login_required
class FollowUsers(View):
    template_name = 'follow_users_forms.html'
    User = get_user_model()
    user_searching = User.objects.all()
    
    def get(self, request, *args, **kwargs):
        user_follows = UserFollows.objects.filter(user=request.user)
        user_followers = UserFollows.objects.filter(followed_user=request.user)
        
        other_users = self.user_searching.exclude(username=request.user)
        for user in user_follows:
            other_users = other_users.exclude(username=user.followed_user)
        
        context = {
            'users': other_users,
            'user_follows': user_follows,
            'user_followers': user_followers
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        user_follows = UserFollows.objects.filter(user=request.user)
        user_followers = UserFollows.objects.filter(followed_user=request.user)
        
        other_users = self.user_searching.exclude(username=request.user)
        for user in user_follows:
            other_users = other_users.exclude(username=user.followed_user)
        
        context = {
            'users': other_users,
            'user_follows': user_follows,
            'user_followers': user_followers
        }
        
        if 'add' in request.POST:
            name = request.POST.getlist('add')[0]
            followed_user = self.user_searching.get(username=name)
            if followed_user in other_users:
                if not UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists():
                    new_followed = UserFollows.objects.create(user=request.user, followed_user=followed_user)
                    return redirect('subscription')
        
        if 'Unsubscribe' in request.POST:
            name = request.POST.get('Unsubscribe')
            user_followed = self.user_searching.get(username=name)
            UserFollows.objects.get(user=request.user, followed_user=user_followed).delete()
            return redirect('subscription')
        
        return render(request, self.template_name, context=context)

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
