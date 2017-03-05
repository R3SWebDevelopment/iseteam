from django import forms

from iseteam.housing.models import Housing

class HousingForm(forms.ModelForm):
	class Meta:
		model = Housing
		widgets = {
			'name' : forms.TextInput(attrs={'class':'form-control'}),
			'last_name' : forms.TextInput(attrs={'class':'form-control'}),
			'country' : forms.TextInput(attrs={'class':'form-control'}),
			'email' : forms.TextInput(attrs={'class':'form-control'}),
			'university' : forms.TextInput(attrs={'class':'form-control'}),
			'people' : forms.Select(attrs={'class':'form-control'}),
			'time_of_stay' : forms.Select(attrs={'class':'form-control'}),
			'date_arrival' : forms.TextInput(attrs={'class':'form-control datepicker'}),
			'amount_pay' : forms.Select(attrs={'class':'form-control'}),
			'live_with' : forms.Select(attrs={'class':'form-control'}),
			'nationality' : forms.Select(attrs={'class':'form-control'}),
			'comments' : forms.Textarea(attrs = {'class' : 'form-control', 'rows':'4'}),
		}
		fields = "__all__" 

