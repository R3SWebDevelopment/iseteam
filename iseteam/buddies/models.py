from django.db import models
from django.contrib.auth.models import User

from iseteam.staff.models import Staff

PERIOD_CHOICES = (

	('Aug13-Dec13','Aug13-Dec13'),
	('Jan14-Jul14','Jan14-Jul14'),
	('Aug14-Dec14','Aug14-Dec14'),
	
	)

class Buddy(models.Model):
	owner = models.ForeignKey(User)
	period = models.CharField(max_length=48, choices=PERIOD_CHOICES)
	staff = models.ManyToManyField(Staff, blank=True, null=True)
	details = models.CharField(max_length=1024)

	def __unicode__(self):
		return u'%s' % (self.owner)


