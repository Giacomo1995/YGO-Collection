from django import forms
from django.forms import TextInput

class CreateSet(forms.Form):
    name = forms.CharField(label='Set Name', max_length=100, widget=forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-large'}))
