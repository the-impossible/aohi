# My Django Imports
from django import forms

# My App imports
from AOHI_users.models import AdoptionInfo
from AOHI_auth.models import Accounts
from AOHI_users.states import states
from AOHI_admin.validator import validate_pic_size
from AOHI_admin.models import Orphans
from AOHI_users.models import Donations

class AdoptionInfoForm(forms.ModelForm):
    state = forms.ChoiceField(choices=states, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    occupation = forms.CharField(required=True, help_text='Please enter your occupation',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    noc = forms.CharField(required=True, help_text='Please enter your current number of children',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number'
        }
    ))

    marital_status = forms.ChoiceField(choices=AdoptionInfo().select_marital, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    gender = forms.ChoiceField(choices=AdoptionInfo().select_gender, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    address = forms.CharField(required=True,help_text='Please enter Home address', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Location where you reside currently',
        }
    ))


    class Meta:
        model = AdoptionInfo
        fields = ('state', 'occupation', 'noc', 'marital_status', 'gender', 'address')

class UserAccountForm(forms.ModelForm):
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

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
                'class':'form-control',
                'type':'file',
                'accept':'image/png, image/jpeg'
            }
        ), validators=[validate_pic_size])

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
        fields = ('firstname', 'lastname', 'email', 'phone', 'password', 'picture')

class UpdateAccountForm(forms.ModelForm):
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

    class Meta:
        model = Accounts
        fields = ('firstname', 'lastname', 'email', 'phone')

class PaymentForm(forms.ModelForm):
    firstname = forms.CharField(required=True, disabled=True,  help_text='Please enter your firstname',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    lastname = forms.CharField(required=True, disabled=True, help_text='Please enter your lastname', widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    email = forms.EmailField(required=True, disabled=True,  help_text='Enter a valid email address', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'email'
        }
    ))

    phone = forms.CharField(required=True, disabled=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number'
        }
    ))

    amount = forms.CharField(required=True, disabled=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number',
            'value':'200000'
        }
    ))

    class Meta:
        model = Accounts
        fields = ('firstname', 'lastname', 'email', 'phone', 'amount')

class AccountPictureForm(forms.ModelForm):
    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = Accounts
        fields = ('picture',)

class OrphanPictureForm(forms.ModelForm):
    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = Orphans
        fields = ('picture',)

class OrphansForm(forms.ModelForm):
    firstname = forms.CharField(required=True, help_text='Please enter child firstname',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    lastname = forms.CharField(required=True,help_text='Please enter child lastname', widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    dob = forms.DateTimeField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'date'
        }
    ))

    gender = forms.ChoiceField(choices=AdoptionInfo().select_gender, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
                'class':'form-control',
                'type':'file',
                'accept':'image/png, image/jpeg'
            }
        ), validators=[validate_pic_size])

    class Meta:
        model = Orphans
        fields = ('firstname', 'lastname', 'dob', 'picture', 'gender')

class UpdateOrphansForm(forms.ModelForm):
    firstname = forms.CharField(required=True, help_text='Please enter child firstname',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    lastname = forms.CharField(required=True,help_text='Please enter child lastname', widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    dob = forms.DateTimeField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'date'
        }
    ))

    gender = forms.ChoiceField(choices=AdoptionInfo().select_gender, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    status = forms.ChoiceField(choices=((True, 'Available'), (False, 'Adopted')), required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    class Meta:
        model = Orphans
        fields = ('firstname', 'lastname', 'dob', 'gender', 'status')

class DonationForm(forms.ModelForm):
    firstname = forms.CharField(required=True,  help_text='Please enter your firstname',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    lastname = forms.CharField(required=True, help_text='Please enter your lastname', widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    email = forms.EmailField(required=True,  help_text='Enter a valid email address', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'email'
        }
    ))

    phone = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number'
        }
    ))

    amount = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number',
        }
    ))

    class Meta:
        model = Donations
        fields = ('firstname', 'lastname', 'email', 'phone', 'amount')
