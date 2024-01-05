from django.contrib.auth.forms import UserCreationForm
from . models import User
from django import forms


class CustomUserForm(UserCreationForm):
    username = forms.RegexField(
        regex=r"^[A-Za-z]\\w{4,14}$",
        error_messages={
            'invalid': 'Username can only contain letters, numbers, and @/./+/-/_ characters.'
        },
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder': 'Enter your username'}),
        label='Username'
    )
    email = forms.EmailField(widget = forms.TextInput(attrs = {'class' :'form-control','placeholder':'Enter Email Address'}))
    password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'class' :'form-control','placeholder':'Enter Your Password'}))
    password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'class' :'form-control','placeholder':'Enter Confirm Password'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']