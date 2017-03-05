from django.forms import ModelForm

from iseteam.pictures.models import Picture

class PictureForm(ModelForm):
	class Meta:
		model = Picture
		fields = '__all__'