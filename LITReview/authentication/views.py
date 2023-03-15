# Create your views here.
from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic

from .forms import SignupForm


class SignUpView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    template_name = "signup.html"
    