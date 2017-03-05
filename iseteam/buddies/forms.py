from django.forms import ModelForm

from iseteam.buddies.models import Buddy

class BuddyForm(ModelForm):
	class Meta:
		model = Buddy
		exclude = ('owner','staff', )
