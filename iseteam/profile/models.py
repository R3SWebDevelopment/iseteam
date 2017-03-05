from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
	user = models.OneToOneField(User)
	country = models.CharField(max_length=124, null=True)
	university = models.CharField(max_length=124, null=True)
	start_period = models.DateField(null=True)
	end_period = models.DateField(null=True)
	is_new = models.BooleanField(default=True)

	
	def __unicode__(self):
		return u'%s' % self.user
