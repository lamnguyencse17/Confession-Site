import datetime

from django.db import models
from django.utils import timezone


class Moderator(models.Model):
    username = models.CharField(max_length=20)
    hash = models.TextField()
    def __str__(self):
        return self.username


class Confession(models.Model):
    confession_text = models.TextField()
    confess_date = models.DateTimeField('date published')
    confession_published = models.TextField(default='Unpublished')
    confession_edited = models.TextField(default='No')
    confession_edited_by = models.ForeignKey(Moderator, on_delete=models.CASCADE, default=(Moderator.objects.get(id=1)))
    confession_edited_date = models.DateTimeField('date edited')
    def __str__(self):
        return self.confession_text

    def was_confessed_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.confess_date <= now
    was_confessed_recently.admin_order_field = 'confess_date'
    was_confessed_recently.boolean = True
    was_confessed_recently.short_description = 'Confessed recently?'


class LoginRecord(models.Model):
    mod = models.ForeignKey(Moderator, on_delete=models.CASCADE)
    date = models.DateTimeField('login date')
    def __str__(self):
        return '{0} {1}'.format(self.mod.username,self.date)
