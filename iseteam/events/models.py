from django.db import models

from autoslug import AutoSlugField

from iseteam.pictures.models import Picture, make_upload_path


class Event(models.Model):
	name = models.CharField(max_length=1024)
	date = models.DateField()
	price_presale = models.IntegerField(blank=True, null=True)
	price_sale = models.IntegerField(blank=True, null=True)
	tickets = models.URLField(max_length=124, blank=True, null=True)
	facebook = models.URLField(max_length=124, blank=True, null=True)
	video = models.URLField(max_length=256, blank=True, null=True)
	cover = models.ImageField(upload_to=make_upload_path)
	brief = models.CharField(max_length=1024)
	description = models.CharField(max_length=10240)
	slug = AutoSlugField(populate_from='name', max_length=255, unique_with='name')


	def __unicode__(self):
		return u'%s' % self.name

	def get_youtube_id(self):
		return self.video.split("v=")[1]

	def get_vimeo_id(self):
		return self.video.split('com/')[1]

	def is_youtube(self):
		if 'youtube' in str(self.video):
			return True
		return False

	def is_vimeo(self):
		if 'vimeo' in str(self.video):
			return True
		return False

	@models.permalink
	def get_absolute_url(self):
		if self.slug:
			return ('view_event', (self.slug,))
		return ('view_event', (self.id,))


