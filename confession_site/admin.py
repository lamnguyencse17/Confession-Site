from django.contrib import admin

from .models import Confession, Moderator, LoginRecord


class Record(admin.StackedInline):
    model = LoginRecord


class ModRecord(admin.ModelAdmin):
    inlines = [Record]


admin.site.register(Confession)
admin.site.register(Moderator, ModRecord)
