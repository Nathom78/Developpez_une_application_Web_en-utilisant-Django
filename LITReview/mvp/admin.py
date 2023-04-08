from django.contrib import admin

# Register your models here.
from .models import Ticket, Review, UserFollows

admin.site.register(UserFollows)
admin.site.register(Ticket)
admin.site.register(Review)
