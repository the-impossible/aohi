# My Django imports
from django.db import models

# My App imports
from AOHI_auth.models import Accounts
from AOHI_users.states import states

# Create your models here.
class AdoptionInfo(models.Model):
    select_gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    select_marital = (
        ('Single', 'Single'),
        ('Married', 'Married'),
    )
    state = models.CharField(max_length=20, choices=states, blank=True, null=True)
    occupation = models.CharField(max_length=30)
    noc = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=10)
    gender = models.CharField(max_length=8, choices=select_gender, blank=True, null=True)
    address = models.TextField(max_length=200)
    updated_date = models.DateTimeField(auto_now_add=True)
    acct = models.OneToOneField(to=Accounts, on_delete=models.CASCADE, blank=True, null=True, related_name="user_acct")
    class Meta:
        verbose_name_plural = 'Adoption Information'
        db_table = 'Adoption Info'

    def __str__(self):
        return f'{self.acct}'

class Donations(models.Model):
    firstname = models.CharField(max_length=30, db_index=True)
    lastname = models.CharField(max_length=30, db_index=True, blank=True)
    phone = models.CharField(max_length=14, unique=False, db_index=True)
    email = models.EmailField(max_length=50, unique=False, verbose_name='email address', db_index=True,blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Donations'
        db_table = 'Donations'

    def __str__(self):
        return f'{self.firstname} donated {self.amount}'