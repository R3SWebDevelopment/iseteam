from django.db import models

from iseteam.pictures.models import Picture, make_upload_path


class Local(models.Model):
	name = models.CharField(max_length=1024)
	place = models.CharField(max_length=124)
	price = models.IntegerField()
	tickets = models.URLField(max_length=124)
	facebook = models.URLField(max_length=124)
	video = models.URLField(max_length=256)
	cover = models.ImageField(upload_to=make_upload_path)
	description = models.CharField(max_length=1024)
	date = models.DateTimeField()

	def __unicode__(self):
		return u'%s' % self.name

	def get_url(self):
		return '/trips/%s/%s' % (self.pk, 'this-is-the-name')

	def get_youtube_id(self):
		return self.video.split("v=")[1]


