from django import forms
from .models import GraphJob, AdjacencyListFile

class ALFileForm(forms.Form):
	file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))