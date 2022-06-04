from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.
class AccountsManager(BaseUserManager):
    def create_user(self, email, firstname, password=None, **kwargs):

        #creates a user with the parameters
        if not email:
            raise ValueError('Email Address required!')

        if password is None:
            raise ValueError('Password is required!')

        if firstname is None:
            raise ValueError('Firstname is required!')

        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, firstname, password):
        # create a superuser with the above parameters
        if password is None:
            raise ValueError('Password should not be empty')

        if firstname is None:
            raise ValueError('Firstname is required!')

        if not email:
            raise ValueError('Email Address required!')

        user = self.create_user(
            email=self.normalize_email(email),
            firstname=firstname,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user

class Accounts(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=30, db_index=True)
    lastname = models.CharField(max_length=30, db_index=True, blank=True)
    phone = models.CharField(max_length=14, unique=True, db_index=True)
    email = models.EmailField(max_length=50, unique=True, verbose_name='email address', db_index=True,blank=True)
    picture = models.ImageField(default='user.png', upload_to='uploaded/', null=True)

    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['firstname']

    objects = AccountsManager()

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    @property
    def imageURL(self):
        try:
            url = self.picture.url
        except:
            url = ''
        return url
    class Meta:
        db_table = 'Accounts'
        verbose_name_plural = 'Accounts'