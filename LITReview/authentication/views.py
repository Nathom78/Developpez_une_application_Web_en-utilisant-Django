# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserCreationForm


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
