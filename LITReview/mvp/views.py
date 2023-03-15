from django.http import HttpResponse
from django.contrib import messages
from itertools import chain
from django.db.models import CharField, Value
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def about(request):
    messages.success(request, 'Profile details updated.')
    return HttpResponse('<h1>À propos</h1> <p>Nous adorons LITReview!</p>')


@login_required
def home(request):
    return render(request, 'home.html')


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



