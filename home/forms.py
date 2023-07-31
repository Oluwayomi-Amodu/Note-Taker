from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import *
from django.contrib.auth import authenticate




class AudioUploadForm(forms.ModelForm):
    audio_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Audio
        fields = ['audio_file']
        labels = {
            'audio_file' : "Audio(wav):",
        }
        


class UserSignupForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=5, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False) # save the details but dont put in database
        user.is_user = True
        user.save()
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your password', 'class': 'form-control'}))

    #def clean(self):
     #   username = self.cleaned_data.get('username')
     #   password = self.cleaned_data.get('password')
     #   user = authenticate(username=username, password=password)
     #   if not user or not user.is_active:
     #       raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
     #   return self.cleaned_data

class NoteEditorForm(forms.ModelForm):
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    note = forms.CharField(label='Text',widget=forms.Textarea( attrs={'class': 'form-control'}))
    class Meta:
        model = Notes
        fields = ['name','note', 'audio']
        labels = {
            'audio' : "Audio(wav):",
        }

class SupportingDocForm(forms.ModelForm):
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    supporting_doc = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Supporting_Doc
        fields = ['name','supporting_doc']