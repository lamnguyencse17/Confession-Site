from django.contrib import admin

from .models import Confession, Moderator

admin.site.register(Confession)
admin.site.register(Moderator)
