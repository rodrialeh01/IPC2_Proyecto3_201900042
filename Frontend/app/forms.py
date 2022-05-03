from django import forms

class FileForm(forms.Form):
    file = forms.FileField(label="file")

class DeleteForm(forms.Form):
    vacio = forms.CharField(label="Vacio")

class AddForm(forms.Form):
    mensaje = forms.CharField(label="mensaje")