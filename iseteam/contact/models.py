from django.db import models

class Contact(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	phone = models.CharField(max_length=255)
	subject = models.CharField(max_length=255)
	comment = models.CharField(max_length=1024)

	def __unicode__(self):
		return u'%s' % self.name