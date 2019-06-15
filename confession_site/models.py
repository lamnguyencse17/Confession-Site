import datetime
import PIL, sys
from PIL import Image
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Moderator(models.Model):
    username = models.CharField(max_length=20)
    hash = models.TextField(default=make_password('toor'))
    def __str__(self):
        return self.username

class Confession(models.Model):
    confession_text = models.TextField()
    confession_picture = models.ImageField(upload_to = 'pictures/', null = True, blank = True, default=None )
    confess_date = models.DateTimeField('date published')
    confession_published = models.TextField(default='Unpublished')
    confession_edited = models.TextField(default='No')
    confession_edited_by = models.ForeignKey(Moderator, on_delete=models.CASCADE, null = True, blank=True, default=None)
    confession_edited_date = models.DateTimeField('date edited')
    def __str__(self):
        return '{0} {1}'.format(self.id, self.confession_text)

    def was_confessed_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.confess_date <= now
    was_confessed_recently.admin_order_field = 'confess_date'
    was_confessed_recently.boolean = True
    was_confessed_recently.short_description = 'Confessed recently?'

    def save(self, *args, **kwargs):
        if self.pk is None and bool(self.confession_picture) is not False:
            basewidth = 1200
            img = Image.open(self.confession_picture)
            exif = None
            if 'exif' in img.info:
                exif = img.info['exif']
            width_percent = (basewidth/float(img.size[0]))
            height_size = int((float(img.size[1])*float(width_percent)))
            img = img.resize((basewidth, height_size), PIL.Image.ANTIALIAS)
            output = BytesIO()
            if exif:
                img.save(output, format='JPEG', exif=exif, quality=85)
            else:
                img.save(output, format='JPEG', quality=85)
            output.seek(0)
            self.confession_picture = InMemoryUploadedFile(output, 'ImageField', "%s" % self.confession_picture.name, 'image/jpeg', sys.getsizeof(output), None)
        super(Confession, self).save()

class LoginRecord(models.Model):
    mod = models.ForeignKey(Moderator, on_delete=models.CASCADE)
    date = models.DateTimeField('login date')
    def __str__(self):
        return '{0} {1}'.format(self.mod.username,self.date)


class ContactRecord(models.Model):
    name = models.TextField()
    email = models.EmailField()
    content = models.TextField()
    date = models.DateTimeField('contacted by', default=timezone.now())
    def __str__(self):
        return '{0} {1}'.format(self.name, self.content)
