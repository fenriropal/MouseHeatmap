from django import forms
from mouseheatmapapp.models import InitialData

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class GetPathForm(forms.ModelForm):
    folder_path = forms.CharField(required=True)
    folder_path.widget = forms.TextInput(attrs={'size': 100, 'title': 'Search',})

    def clean_renewal_date(self):
        data = self.cleaned_data['folder_path']

        # Check if a date is not empty.
        if data == "":
            raise ValidationError(_('Invalid folder path - empty path'))

        # Remember to always return the cleaned data.
        return data

    class Meta:
        model = InitialData
        fields = ['folder_path']
