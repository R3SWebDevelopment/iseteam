from django.forms import ModelForm
from django.forms.widgets import SplitDateTimeWidget

from iseteam.local.models import Local

class LocalForm(ModelForm):
	class Meta:
		model = Local
		widgets = {'date': SplitDateTimeWidget(date_format='%d/%m/%Y')}
