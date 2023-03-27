"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
For internalization url see 1.3):
https://makina-corpus.com/django/internationalisation-avec-django

"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView)

import authentication.views
import mvp.views


urlpatterns = [
    path('home', mvp.views.home, name='home'),
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(template_name="logged_out.html"), name='logout'),
    path("signup/", authentication.views.SignUpView.as_view(template_name="signup.html"), name="signup"),
    path('password_change/', PasswordChangeView.as_view(
        template_name='password_change_form.html'),
         name='password_change'
         ),
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'),
         name='password_change_done'
         ),
    path('password_reset/', PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
        ),
         name='password_reset'
        ),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        post_reset_login=True,
        success_url='home'
        ),
         name='password_reset_confirm'),
    # If case post_reset_login=default and success_url=default we can use reset/done (complete)
    # path('reset/done', PasswordResetCompleteView.as_view(
    #      template_name='password_reset_complete.html'),
    #      name='password_reset_complete')
    path('subscription/', mvp.views.FollowUsers.as_view(), name='subscription'),
]
