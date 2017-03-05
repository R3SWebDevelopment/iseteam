from django.db import models

PEOPLE_CHOICES = (
('1','ONE'),
('2','TWO'),
('3','THREE'),
('4','FOUR'),
('4+','MORE THAN 4'),
	)

TIME_CHOICES = (
('ONE SEMESTER', 'ONE SEMESTER'),
('TWO SEMESTERS', 'TWO SEMESTERS'),
('MORE THAN ONE YEAR', 'MORE THAN ONE YEAR'),
	)

AMOUNT_CHOICES = (
('$4000','$4000 MXN'),
('$5000','$5000 MXN'),
('$6000','$6000 MXN'),
('$7000','$7000 MXN'),
('MORE THAN $7000','MORE THAN $7000 MXN'),
	)

LIVE_CHOICES = (
('MEN','MEN'),
('WOMEN', 'WOMEN'),
('BOTH', 'BOTH'),
	)

NATIONALITY_CHOICES = (
('MEXICAN', 'MEXICAN'),
('INTERNATIONAL', 'INTERNATIONAL'),
	)

class Housing(models.Model):
	name =  models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	country = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	university = models.CharField(max_length=255)
	people = models.CharField(max_length=5, choices=PEOPLE_CHOICES)
	time_of_stay = models.CharField(max_length=32, choices=TIME_CHOICES)
	date_arrival = models.DateField()
	amount_pay = models.CharField(max_length=32, choices=AMOUNT_CHOICES)
	live_with = models.CharField(max_length=32, choices=LIVE_CHOICES)
	comments = models.CharField(max_length=1024)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s' % self.name



