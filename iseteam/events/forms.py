from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select, FileInput

from iseteam.events.models import Event

class EventForm(ModelForm):
	class Meta:
		model = Event
		exclude = ('slug',)
		widgets = {
			'name' : TextInput(attrs={'placeholder':'Event Name', 'class':'form-control'}),
			'date' : TextInput(attrs={'placeholder':'Date', 'class':' datepicker form-control'}),
			'price_presale' : TextInput(attrs={'placeholder':'Price Pre-sale', 'class':'form-control'}),
			'price_sale' : TextInput(attrs={'placeholder':'Price Sale', 'class':'form-control'}),
			'tickets' : TextInput(attrs={'placeholder':'Tickets URL', 'class':'form-control'}),
			'facebook' : TextInput(attrs={'placeholder':'Facebook URL', 'class':'form-control'}),
			'video' : TextInput(attrs={'placeholder':'Youtube URL', 'class':'form-control'}),
			'cover' : FileInput(attrs={'placeholder':'Vertical Cover', 'class':'form-control'}),
			'brief' : Textarea(attrs={'placeholder':'Brief','class':'form-control', 'rows':'5'}),
			'description' : Textarea(attrs={'placeholder':'Description','class':'textarea-html'}),
		}







