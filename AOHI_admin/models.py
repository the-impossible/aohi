# My django imports
from django.db import models

# My app imports
from AOHI_auth.models import Accounts
from AOHI_users.models import AdoptionInfo
# Create your models here.
class Orphans(models.Model):
    firstname = models.CharField(max_length=30, db_index=True)
    lastname = models.CharField(max_length=30, db_index=True, blank=True)
    dob = models.DateField(auto_now=False)
    picture = models.ImageField(default='user.png', null=True, upload_to='uploaded/')
    gender = models.CharField(max_length=8, choices=AdoptionInfo().select_gender, blank=True, null=True)
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def imageURL(self):
        try:
            url = self.picture.url
        except:
            url = ''
        return url

    class Meta:
        verbose_name_plural = 'Orphans'
        db_table = 'Orphans'

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

class Adoptions(models.Model):
    orphan = models.ForeignKey(to=Orphans, on_delete=models.CASCADE, blank=True, null=True, related_name="adopt_orphan")
    user = models.ForeignKey(to=Accounts, on_delete=models.CASCADE, blank=True, null=True, related_name="user_adopt_acct")
    status = models.BooleanField(default=False)
    adopted_date = models.DateField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Adoptions'
        db_table = 'Adoptions'

    def __str__(self):
        return f'Adoption({self.status}) for {self.user} on {self.orphan}'

class RequestAdoption(models.Model):
    orphan = models.ForeignKey(to=Orphans, on_delete=models.CASCADE, blank=True, null=True, related_name="request_orphan")
    user = models.ForeignKey(to=Accounts, on_delete=models.CASCADE, blank=True, null=True, related_name="request_acct")
    status = models.BooleanField(default=False)
    adopted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Request Adoption'
        db_table = 'Request Adoption'

    def __str__(self):
        return f'{self.user} Requested for {self.orphan}'

class Payments(models.Model):
    orphan = models.ForeignKey(to=Orphans, on_delete=models.CASCADE, blank=True, null=True, related_name="orphan_payment")
    user = models.ForeignKey(to=Accounts, on_delete=models.CASCADE, blank=True, null=True, related_name="user_paid_acct")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    adopted_date = models.DateTimeField(auto_now_add=True)
    date_paid = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Payments'
        db_table = 'Payments'

    def __str__(self):
        return f'{self.user} paid for {self.orphan}'