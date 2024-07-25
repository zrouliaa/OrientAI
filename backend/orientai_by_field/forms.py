from django import forms

class FieldForm(forms.Form):
    field = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter a field of study'}),
        label='Field of Study'
    )
