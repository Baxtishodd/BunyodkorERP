from django.contrib import admin
from .models import Record, Product, Contact, Account, Lead

# from django.contrib.auth.admin import UserAdmin

# Change the title and header
admin.site.site_header = "BunyodCore Platform"
admin.site.site_title = "BunyodCore Platform"
admin.site.index_title = "BunyodCore Platform | created by Bakhtishod"

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'birthday', 'phone', 'sex', 'country', 'state', 'city', 'id']
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('email', 'sex', 'country', 'state', 'city')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company', 'lead_status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company__account_name')
    list_filter = ('lead_status', 'industry', 'account_manager', 'created_at')

    # Make 'created_by' read-only so it cannot be manually edited
    readonly_fields = ['created_by', 'created_at']

    # Automatically assign 'created_by' to the current user on save
    def save_model(self, request, obj, form, change):
        if not change:  # If it's a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    # def get_company_name(self, obj):
    #     return obj.company.account_name if obj.company else None
    #
    # get_company_name.short_description = 'Company Name'


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'director', 'industry', 'phone', 'website', 'annual_revenue', 'account_manager', 'created_at')
    list_filter = ('industry', 'account_manager', 'created_at')
    search_fields = ('account_name', 'industry', 'phone', 'website', 'annual_revenue')
    ordering = ('-created_at',)
    # filter_horizontal = ('contacts',)

    fieldsets = (
        (None, {
            'fields': ('account_name', 'director', 'industry', 'website', 'phone', 'address', 'description', 'annual_revenue', 'account_manager', 'contacts')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'account_manager')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('lead_name', 'company_name', 'email', 'phone', 'status', 'source', 'account_manager', 'created_at')
    list_filter = ('status', 'source', 'account_manager', 'created_at')
    search_fields = ('lead_name', 'company_name', 'email', 'phone', 'account_manager__username')
    ordering = ('-created_at',)


# admin.site.register(Contact, ContactAdmin)
# admin.site.register(Record, RecordAdmin)
admin.site.register(Product)

