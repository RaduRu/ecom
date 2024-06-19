from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from .models import Customer


class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )


