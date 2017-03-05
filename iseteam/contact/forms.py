from django import forms
from django.forms import ModelForm

from iseteam.contact.models import Contact

class ContactForm(ModelForm):
	class Meta:
		model = Contact
		fields = "__all__" 





