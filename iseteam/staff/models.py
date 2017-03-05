# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from iseteam.pictures.models import Picture, make_upload_path

AGE_CHOICES = (

	('18 years old','18 years old' ),
	('19 years old','19 years old' ),
	('20 years old','20 years old' ),
	('21 years old','21 years old' ),
	('22 years old','22 years old' ),
	('23 years old','23 years old' ),
	('24 years old','24 years old' ),
	('25 years old','25 years old' ),
	('26 years old','26 years old' ),
	('27 years old','27 years old' ),
	('28 years old','28 years old' ),
	('29 years old','29 years old' ),
	('30 years old','30 years old' ),
	('30+','30+' ),	
	)

GENDER_CHOICES = (
	('MALE', 'MALE'),
	('FEMALE', 'FEMALE'),
	)

Q2_CHOICES = (
	('Taker', 'Taker'),
	('Giver', 'Giver'),
	)

Q3_CHOICES = (
	('life is a party, crash it', 'life is a party, crash it'),
	('He who does not live to serve does not deserve to live','He who does not live to serve does not deserve to live'),
	('Dont stay in bed, unless you can make money in bed', 'Dont stay in bed, unless you can make money in bed'),
	)

Q5_CHOICES = (
	('A 10 million dolar mansion','A 10 million dolar mansion'),
	('A 500k USD car','A 500k USD car'),
	('One round world ticket','One round world ticket'),
	)

Q6_CHOICES = (
	('Never','Never'),
	('Rarely','Rarely'),
	('Indifferent','Indifferent'),
	('Sometimes','Sometimes'),
	('Always','Always'),
	)

Q7_CHOICES = (
	('Safety first','Safety first'),
	('Adventure is out there','Adventure is out there'),
	('A pear in hand is better than a pear in the bush','A pear in hand is better than a pear in the bush'),
	)

Q8_CHOICES = (
	('Sir yes sir! doing exactly what is expected of you. A good soldier who follows orders makes for a strong team','Sir yes sir! doing exactly what is expected of you. A good soldier who follows orders makes for a strong team'),
	('Not taking no for an answer, going above and beyond your duty in order to best benefit your team','Not taking no for an answer, going above and beyond your duty in order to best benefit your team'),
	)

Q9_CHOICES = (
	('If you do not ask the question, the answer will always be no','If you do not ask the question, the answer will always be no'),
	('When life gives you lemons, make lemonade','When life gives you lemons, make lemonade'),
	('Go with the flow','Go with the flow')
	)

Q10_CHOICES = (
	('To each their own','To each their own'),
	('I wonder what troubles him/her?','I wonder what troubles him/her?'),
	)

Q24_CHOICES = (
	('YES','YES'),
	('NO','NO'),
	)



class Staff(models.Model):
	name = models.CharField(max_length=255)
	position = models.CharField(max_length=255)
	photo = models.ImageField(upload_to=make_upload_path)
	age = models.IntegerField()
	carrer = models.CharField(max_length=255)
	school = models.CharField(max_length=255)
	hometown = models.CharField(max_length=255)
	phone = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	facebook = models.URLField(max_length=255)
	
	def __unicode__(self):
		return u'%s' % self.name


class UserStaff(models.Model):
	username = models.CharField(max_length=255)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	password = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % self.name


class JoinUs(models.Model):
	name = models.CharField(max_length=255)
	fb = models.URLField(max_length=255, blank=True, null=True)
	email = models.EmailField(max_length=255)
	mobile = models.CharField(max_length=255)
	nationality = models.CharField(max_length=255)
	age = models.CharField(max_length=255, choices=AGE_CHOICES)
	gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
	occupation = models.CharField(max_length=255)
	school = models.CharField(max_length=255)
	languages = models.CharField(max_length=255)
	question1 = models.CharField(max_length=255)
	question2 = models.CharField(max_length=255, choices=Q2_CHOICES)
	question3 = models.CharField(max_length=255, choices=Q3_CHOICES)
	question4 = models.CharField(max_length=255)
	question5 = models.CharField(max_length=255, choices=Q5_CHOICES)
	question6 = models.CharField(max_length=255, choices=Q6_CHOICES)
	question7 = models.CharField(max_length=255, choices=Q7_CHOICES)
	question8 = models.CharField(max_length=255, choices=Q8_CHOICES)
	question9 = models.CharField(max_length=255, choices=Q9_CHOICES)
	question10 = models.CharField(max_length=255, choices=Q10_CHOICES)
	question11= models.CharField(max_length=255)
	points = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % self.name


class JoinUs2(models.Model):
	name = models.CharField(max_length=255)
	fb = models.URLField(max_length=255, blank=True, null=True)
	email = models.EmailField(max_length=255)
	mobile = models.CharField(max_length=255)
	nationality = models.CharField(max_length=255)
	age = models.CharField(max_length=255, choices=AGE_CHOICES)
	gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
	occupation = models.CharField(max_length=255)
	school = models.CharField(max_length=255)
	languages = models.CharField(max_length=255)

	question11 = models.CharField(max_length=255)
	question12 = models.CharField(max_length=255, choices=Q3_CHOICES)
	question13 = models.CharField(max_length=255)
	question14 = models.CharField(max_length=255, choices=Q7_CHOICES)
	question15 = models.CharField(max_length=255, choices=Q8_CHOICES)
	question16 = models.CharField(max_length=255, choices=Q9_CHOICES)
	question17 = models.CharField(max_length=255, choices=Q10_CHOICES)
	question18 = models.CharField(max_length=255)
	question19 = models.CharField(max_length=255)
	question20 = models.CharField(max_length=255)
	question21= models.CharField(max_length=255)
	question22= models.CharField(max_length=255)
	question23= models.CharField(max_length=255)
	question24= models.CharField(max_length=255, choices=Q24_CHOICES)
	points = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % self.name




		
