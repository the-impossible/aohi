from django.contrib import admin

# My App imports
from AOHI_admin.models import Adoptions, Orphans, Payments, RequestAdoption

# Register your models here.
class AdoptionsAdmin(admin.ModelAdmin):
    model = Adoptions
    list_display = ('__str__', 'orphan', 'user', 'status', 'adopted_date', 'date_created')
    search_fields = ('orphan', 'status','user')
    list_filter = ('date_created',)

class RequestAdoptionAdmin(admin.ModelAdmin):
    model = RequestAdoption
    list_display = ('__str__', 'orphan', 'user', 'status', 'adopted', 'date_created',)
    search_fields = ('orphan', 'status','user')
    list_filter = ('date_created',)


class OrphansAdmin(admin.ModelAdmin):
    model = Orphans
    list_display = ('__str__', 'firstname', 'lastname',)
    search_fields = ('firstname', 'lastname',)
    list_filter = ('date_created',)

class PaymentsAdmin(admin.ModelAdmin):
    model = Payments
    list_display = ('__str__', 'orphan', 'user', 'amount')
    search_fields = ('user', 'amount', 'orphan')
    list_filter = ('adopted_date',)

# Register your models here.
admin.site.register(Adoptions, AdoptionsAdmin)
admin.site.register(Orphans, OrphansAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(RequestAdoption, RequestAdoptionAdmin)