from django.forms import ModelForm
from django.forms.widgets import SplitDateTimeWidget


from iseteam.parties.models import Party

class PartyForm(ModelForm):
	class Meta:
		model = Party
		widgets = {'date': SplitDateTimeWidget(date_format='%d/%m/%Y')}
		fields = "__all__" 
