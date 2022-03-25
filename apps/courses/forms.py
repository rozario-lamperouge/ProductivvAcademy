from django import forms

class NameForm(forms.Form):
    Full_Name = forms.CharField(label='Full Name', max_length=100)