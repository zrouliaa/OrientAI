from django import forms

class MarkForm(forms.Form):
    level = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Bac Sciences Maths B'}))
    subjects = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Mathematics'}))
    scores = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Score'}))
