from django.db import models

class Album(models.Model):
	name = models.CharField(max_length=255)
	datetime = models.DateField(auto_now_add=True)
