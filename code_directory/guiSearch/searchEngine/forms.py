from django import forms

# This is the form for the add_data html page
class AddDataForm(forms.Form):
    appName = forms.CharField(label="", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Application Name'}))
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
