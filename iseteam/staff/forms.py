from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select, FileInput, CheckboxInput

from iseteam.staff.models import Staff, JoinUs, JoinUs2


class NewMemberForm(forms.Form):
	username = forms.CharField(
		widget = TextInput(attrs={'class':'form-control'})
		)
	first_name = forms.CharField(
		widget = forms.TextInput(attrs={'class':'form-control'})
		)
	last_name = forms.CharField(
		widget = forms.TextInput(attrs={'class':'form-control'})
		)
	password = forms.CharField(
		widget = forms.PasswordInput(attrs={'class':'form-control'})
		)
	is_superuser = forms.BooleanField(
		widget = forms.CheckboxInput(attrs={'class':''},),
		required=False,
		)



class StaffForm(ModelForm):
	class Meta:
		model = Staff
		widgets = {
			'name' : TextInput(attrs={'placeholder':'Full Name', 'class':'form-control'}),
			'position' : TextInput(attrs={'placeholder':'Position', 'class':'form-control'}),
			'photo' : FileInput(attrs={'placeholder':'Photo', 'class':'form-control'}),
			'age' : TextInput(attrs={'placeholder':'Age', 'class':'form-control'}),
			'carrer' : TextInput(attrs={'placeholder':'Carrer', 'class':'form-control'}),
			'school' : TextInput(attrs={'placeholder':'School', 'class':'form-control'}),
			'hometown' : TextInput(attrs={'placeholder':'hometown', 'class':'form-control'}),
			'phone' : TextInput(attrs={'placeholder':'Phone', 'class':'form-control'}),
			'email' : TextInput(attrs={'placeholder':'Email', 'class':'form-control'}),
			'facebook' : TextInput(attrs={'placeholder':'Facebook URL', 'class':'form-control'}),
		}
		fields = "__all__" 


class JoinUsForm(ModelForm):
	class Meta:
		model = JoinUs
		exclude = ('date', 'points')
		widgets = {
			'name' : TextInput(attrs={'class':'form-control'}),
			'fb' : TextInput(attrs={'class':'form-control'}),
			'email' : TextInput(attrs={'class':'form-control'}),
			'mobile' : TextInput(attrs={'class':'form-control'}),
			'nationality' : TextInput(attrs={'class':'form-control'}),
			'age' : forms.Select(attrs={'class':'form-control'}),
			'gender' : forms.Select(attrs={'class':'form-control'}),
			'occupation' : TextInput(attrs={'class':'form-control'}),
			'school' : TextInput(attrs={'class':'form-control'}),
			'languages' : TextInput(attrs={'class':'form-control'}),
			'question1' : forms.Textarea(attrs = {'class' : 'form-control col-md-12', 'rows':'4'}),
			'question2' : forms.Select(attrs={'class':'form-control'}),
			'question3' : forms.Select(attrs={'class':'form-control'}),
			'question4' : forms.Textarea(attrs = {'class' : 'form-control', 'rows':'4'}),
			'question5' : forms.Select(attrs={'class':'form-control'}),
			'question6' : forms.Select(attrs={'class':'form-control'}),
			'question7' : forms.Select(attrs={'class':'form-control'}),
			'question8' : forms.Select(attrs={'class':'form-control'}),
			'question9' : forms.Select(attrs={'class':'form-control'}),
			'question10' : forms.Select(attrs={'class':'form-control'}),
			'question11' : forms.Textarea(attrs = {'class' : 'form-control', 'rows':'4'}),

		}


class JoinUs2Form(ModelForm):
	class Meta:
		model = JoinUs2
		exclude = ('date', 'points')
		widgets = {
			'name' : TextInput(attrs={'class':'form-control'}),
			'fb' : TextInput(attrs={'class':'form-control'}),
			'email' : TextInput(attrs={'class':'form-control'}),
			'mobile' : TextInput(attrs={'class':'form-control'}),
			'nationality' : forms.Select(attrs={'class':'form-control'}),
			'age' : forms.Select(attrs={'class':'form-control'}),
			'gender' : forms.Select(attrs={'class':'form-control'}),
			'occupation' : TextInput(attrs={'class':'form-control'}),
			'school' : TextInput(attrs={'class':'form-control'}),
			'languages' : TextInput(attrs={'class':'form-control'}),

			'question11' : forms.Textarea(attrs = {'class' : 'form-control col-md-12', 'rows':'4'}),
			'question12' : forms.Select(attrs={'class':'form-control'}),
			'question13' : forms.Textarea(attrs = {'class' : 'form-control col-md-12', 'rows':'4'}),
			'question14' : forms.Select(attrs={'class':'form-control'}),
			'question15' : forms.Select(attrs={'class':'form-control'}),
			'question16' : forms.Select(attrs={'class':'form-control'}),
			'question17' : forms.Select(attrs={'class':'form-control'}),
			'question18' : forms.Textarea(attrs = {'class' : 'form-control col-md-12', 'rows':'4'}),
			'question19' : forms.Textarea(attrs = {'class' : 'form-control col-md-12', 'rows':'4'}),
			'question20' : forms.Textarea(attrs = {'class' : 'form-control col-md-12', 'rows':'4'}),
			'question21' : forms.Textarea(attrs = {'class' : 'form-control col-md-12', 'rows':'4'}),
			'question22' : forms.Textarea(attrs = {'class' : 'form-control col-md-12', 'rows':'4'}),
			'question23' : forms.Textarea(attrs = {'class' : 'form-control col-md-12', 'rows':'4'}),
			'question24' : forms.Select(attrs={'class':'form-control'}),
		}






