from django.views.generic.list import ListView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.db.models import CharField, Value
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy

from itertools import chain

from .models import UserFollows, Ticket, Review
from .forms import ReviewForm, ReviewUpdateForm, TicketForm


@login_required
def home(request):
    return render(request, 'home.html')


def get_users_viewable_reviews(the_user):
    """
    Take User for return all reviews who can see, else all if administrator, or just followed users' reviews
    """
    all_user_follows = UserFollows.objects.filter(user=the_user)
    all_user_permitted = [couple.followed_user for couple in all_user_follows]
    reviews = Review.objects.filter(user__in=all_user_permitted)
    if the_user.groups.filter(name='administrators').exists():
        reviews = Review.objects.exclude(user=the_user)
    return reviews


def get_users_viewable_tickets(the_user):
    """
    Take User for return all reviews who can see, else all if administrator, or just followed users' reviews
    """
    all_user_follows = UserFollows.objects.filter(user=the_user)
    all_user_permitted = [couple.followed_user for couple in all_user_follows]
    tickets = Ticket.objects.filter(user__in=all_user_permitted)
    if the_user.groups.filter(name='administrators').exists():
        tickets = Ticket.objects.exclude(user=the_user)
    return tickets


class Stream(LoginRequiredMixin, ListView):
    paginate_by = 4

    def get_queryset(self):
        reviews = get_users_viewable_reviews(self.request.user)
        # returns queryset of reviews
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        tickets = get_users_viewable_tickets(self.request.user)
        # returns queryset of tickets
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # combine and sort the two types of posts
        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )
        return posts


class MyFormCreateTicketView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    success_url = 'stream'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MyFormCreateTicketView, self).form_valid(form)


class MyFormsCreateTicketReviewView(LoginRequiredMixin, CreateView):
    form_class_ticket = TicketForm
    form_class = ReviewForm
    template_name = 'mvp/ticket_review_form.html'
    success_url = 'stream'

    def get_context_data(self, **kwargs):
        context_data = super(MyFormsCreateTicketReviewView, self).get_context_data(**kwargs)
        context_data.update(
            {
                'ticket_form': self.form_class_ticket,
            }
        )
        return context_data

    def post(self, request, *args, **kwargs):
        form_review = self.get_form(form_class=ReviewForm)
        form_ticket = self.get_form(form_class=TicketForm)
        self.object = None

        if form_ticket.is_valid():
            form_ticket.instance.user = self.request.user
            form_ticket.save()
        else:
            return self.form_invalid(form_ticket)

        if form_review.is_valid():
            form_review.instance.user = self.request.user
            form_review.instance.ticket = Ticket.objects.get(id=form_ticket.instance.id)
            return self.form_valid(form_review)
        else:
            return self.form_invalid(form_review)


class MyFormsCreateReviewView(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = 'mvp/review_form.html'
    success_url = '/stream'

    def dispatch(self, request, *args, **kwargs):
        self.ticket = Ticket.objects.get(pk=kwargs['ticket_id'])
        return super(MyFormsCreateReviewView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(MyFormsCreateReviewView, self).get_context_data(**kwargs)
        context_data.update(
            {
                'ticket': self.ticket,
            }
        )
        return context_data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = None
        if form.is_valid():
            form.instance.user = self.request.user
            form.instance.ticket = self.ticket
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Posts(LoginRequiredMixin, ListView):
    paginate_by = 4

    def get_queryset(self):
        reviews = Review.objects.filter(user=self.request.user)
        # returns queryset of reviews
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        tickets = Ticket.objects.filter(user=self.request.user)
        # returns queryset of tickets
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # combine and sort the two types of posts
        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )
        return posts


class MyFormUpdateTicketView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('posts')
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                'ticket': Ticket.objects.get(pk=self.object.id)
            }
        )
        return context_data


class MyFormDeleteTicketView(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('posts')

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(self.request)


class MyFormUpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewUpdateForm
    success_url = reverse_lazy('posts')
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context_data = super(MyFormUpdateReviewView, self).get_context_data(**kwargs)
        context_data.update(
            {
                'ticket': Ticket.objects.get(pk=self.object.ticket.id)
            }
        )
        return context_data


class MyFormDeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('posts')


class FollowUsers(LoginRequiredMixin, View):
    template_name = ''
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
            try:
                followed_user = self.user_searching.get(username=name)
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, _("User doesn't exist."))
            else:
                if followed_user in other_users:
                    if not UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists():
                        new_user_follows = UserFollows(user=request.user, followed_user=followed_user)
                        new_user_follows.save()
                        # UserFollows.objects.create(user=request.user, followed_user=followed_user)
                        return redirect('subscription')
                elif followed_user == request.user:
                    messages.add_message(request, messages.ERROR, _("It can't be yourself."))
                elif followed_user not in other_users:
                    messages.add_message(request, messages.ERROR, _("User is already followed."))

        if 'Unsubscribe' in request.POST:
            name = request.POST.get('Unsubscribe')
            user_followed = self.user_searching.get(username=name)
            UserFollows.objects.get(user=request.user, followed_user=user_followed).delete()
            return redirect('subscription')

        return render(request, self.template_name, context=context)
