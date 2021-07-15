from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), help_text='')
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), help_text='')
    new_password2 = forms.CharField(label='New Password Confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), help_text='')
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb-3'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), help_text='')
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), help_text='')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control mb-3'})
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control mb-3'})
        }