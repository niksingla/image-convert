from django import forms
from .models import FileUpload

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file_field']
        labels = {
            'file_field':''
        }
        Widgets = {
            'file_upload':forms.FileField()
        }
