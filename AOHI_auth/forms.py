# My Django Imports
from django import forms

# My App imports
from AOHI_auth.models import Accounts

class AccountCreationForm(forms.ModelForm):
    firstname = forms.CharField(required=True, help_text='Please enter your firstname',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    lastname = forms.CharField(required=True,help_text='Please enter your lastname', widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    email = forms.EmailField(required=True, help_text='Enter a valid email address', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'email'
        }
    ))

    phone = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number'
        }
    ))

    password = forms.CharField(required=True, help_text='Password must contain at least 6 characters',
    widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'Password',
        }
    ))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('Password too short, should be at least 6 characters!')

        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Accounts.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Already taken!')

        return email

    class Meta:
        model = Accounts
        fields = ('firstname', 'lastname', 'email', 'phone', 'password')