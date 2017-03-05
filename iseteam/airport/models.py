from django.db import models
from django.contrib.auth.models import User

PEOPLE_CHOICES = (
('1','ONE'),
('2','TWO'),
('3','THREE'),
('4','FOUR'),
('4+','MORE THAN 4'),
	)


CITY_CHOICES = (
	('Mty','Monterrey'),
	('Qro','Queretaro'),
)

"""
Anonymous user pick up class
"""
class PickUp(models.Model):
	city = models.CharField(max_length=255, choices=CITY_CHOICES, default='Mty',blank=True, null=True)
	name = models.CharField(max_length=124)
	last_name = models.CharField(max_length=124)
	country = models.CharField(max_length=124)
	email = models.EmailField(max_length=124)
	flight_number = models.CharField(max_length=124)
	airline = models.CharField(max_length=124)
	terminal = models.CharField(max_length=124)
	people = models.CharField(max_length=5, choices=PEOPLE_CHOICES)
	date =  models.DateField()
	time = models.TimeField()
	comments = models.CharField(max_length=1024)
	timestamp = models.DateTimeField(auto_now_add=True)
	attendant = models.ForeignKey(User, blank=True, null=True)


	def __unicode__(self):
		return u'%s' % self.name








