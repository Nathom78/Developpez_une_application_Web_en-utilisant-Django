from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages


def hello(request):
    return HttpResponse('<h1>Hello Django!</h1>')


def about(request):
    messages.success(request, 'Profile details updated.')
    return HttpResponse('<h1>À propos</h1> <p>Nous adorons LITReview!</p>')

