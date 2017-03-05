from django.forms import ModelForm

from iseteam.profile.models import Profile


class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		exclude = ('user', 'is_new',)