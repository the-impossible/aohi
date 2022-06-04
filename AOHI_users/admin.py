from django.contrib import admin

# My App imports
from AOHI_users.models import AdoptionInfo, Donations

# Register your models here.
class AdoptionInfoAdmin(admin.ModelAdmin):
    model = AdoptionInfo
    list_display = ('__str__', 'acct', 'gender', 'occupation', 'noc', 'marital_status')
    search_fields = ('acct', 'noc','gender')
    list_filter = ('updated_date',)

class DonationsAdmin(admin.ModelAdmin):
    model = Donations
    list_display = ('__str__', 'firstname', 'lastname', 'email', 'amount', 'phone')
    search_fields = ('email', 'phone','amount')
    list_filter = ('amount',)

admin.site.register(AdoptionInfo, AdoptionInfoAdmin)
admin.site.register(Donations, DonationsAdmin)