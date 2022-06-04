from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# My App imports
from AOHI_auth.models import Accounts
from AOHI_admin.forms import UpdateAccountForm

# Register your models here.
class AccountsAdmin(UserAdmin):
    list_display = ('email', 'firstname', 'lastname', 'date_joined', 'last_login', 'is_active', 'is_staff', )
    search_fields = ('email', 'firstname',)
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    # fieldsets = (
    #     (None, {'fields': ('email', 'firstname', 'lastname', 'password', 'phone', 'picture')}),
    # )

    # form = UpdateAccountForm
    # add_form = UpdateAccountForm

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'firstname', 'lastname', 'password', 'phone', 'picture'),
    #     }),
    # )

# Register your models here.
admin.site.register(Accounts, AccountsAdmin)