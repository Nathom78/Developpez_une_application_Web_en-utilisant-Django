# Create your views here.
from django.conf import settings
from django.contrib.auth.models import Group

from django.urls import reverse_lazy
from django.views import generic

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate
from django.contrib.messages.views import SuccessMessageMixin

from .forms import UserCreationForm


# class SignUpView(SuccessMessageMixin, View):
#     form_class = SignupForm
#     success_message = "You have successfully created an account!"
#     template_name = "signup.html"
#
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # Do not save to table yet
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#
#             try:
#                 validate_password(password, user)
#             except ValidationError as e:
#                 form.add_error('password1', e)  # to be displayed with the field's errors
#                 return render(request, self.template_name, {'form': form})
#             user.save()
#             # Let's try to login the user
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#             return redirect(settings.LOGIN_REDIRECT_URL)
#         return render(request, self.template_name, {'form': form, 'message': message})
#
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    
    