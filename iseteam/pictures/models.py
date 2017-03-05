import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from iseteam.pictures.thumbs import ImageWithThumbsField



def make_upload_path(instance, filename):
    file_root, file_ext = os.path.splitext(filename)
    dir_name = '{module}/{model}'.format(module=instance._meta.app_label, model=instance._meta.app_label)
    file_root = unicode(uuid.uuid4())
    name = os.path.join(settings.MEDIA_ROOT, 'images' ,dir_name, file_root + file_ext.lower())
    # Delete existing file to overwrite it later
    if instance.pk:
        while os.path.exists(name):
            os.remove(name)

    return os.path.join(dir_name, file_root + file_ext.lower())

class Picture(models.Model):
    picture = ImageWithThumbsField(upload_to=make_upload_path, sizes=((120,120),(200,200)))
    #owner = models.ForeignKey(User)
    #date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.picture.url

    #def get_url(self):
    #    return str(self.picture.url).split("?")[0]

