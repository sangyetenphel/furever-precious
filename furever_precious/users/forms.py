from django.db.models.query_utils import FilteredRelation
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, widgets
from django.forms.fields import EmailField
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    # Adding email to UserCreationForm besides the default of username and password
    email = forms.EmailField()

    class Meta:
        # Save to User model after we form.save()
        model = User
        # Fields to display in order in front-end
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control mb-3'})
        }