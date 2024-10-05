from django.contrib import admin
from .models import Record, Product, Contact

# from django.contrib.auth.admin import UserAdmin

# Change the title and header
admin.site.site_header = "BunyodCore Platform"
admin.site.site_title = "BunyodCore Platform"
admin.site.index_title = "BunyodCore Platform | created by Bakhtishod"

class RecordAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'birthday', 'phone', 'sex', 'country', 'state', 'city', 'id']
    search_fields = ('first_name', 'last_name', 'email', 'phone')



class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company_name', 'lead_status')
    search_fields = ('first_name', 'last_name', 'email', 'company_name')
    list_filter = ('lead_status', 'industry', 'account_manager')

    # Make 'created_by' read-only so it cannot be manually edited
    readonly_fields = ['created_by']

    # Automatically assign 'created_by' to the current user on save
    def save_model(self, request, obj, form, change):
        if not change:  # If it's a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Contact, ContactAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Product)

