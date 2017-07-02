from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    myClass = forms.CharField(widget=forms.TextInput(attrs={'class' : 'addAppForm'}))
    file = forms.FileField()
