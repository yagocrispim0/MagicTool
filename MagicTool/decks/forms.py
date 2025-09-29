from django import forms
from .models import Deck, Card

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'format']

        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
        }