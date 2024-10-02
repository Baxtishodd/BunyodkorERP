from django.contrib import admin
from .models import Record, Product, Contact

# from django.contrib.auth.admin import UserAdmin


class RecordAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'birthday', 'phone', 'sex', 'country', 'state', 'city', 'id']
    search_fields = ('first_name', 'last_name', 'email', 'phone')



class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company_name', 'lead_status')
    search_fields = ('first_name', 'last_name', 'email', 'company_name')
    list_filter = ('lead_status', 'industry', 'account_manager')

admin.site.register(Contact, ContactAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Product)

