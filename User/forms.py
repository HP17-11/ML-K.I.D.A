from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import filedata, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class FiledataForm(forms.ModelForm):
    class Meta:
        model = filedata
        fields = ['video_file']

    def __init__(self, *args, **kwargs):
        super(FiledataForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'id': 'video'})