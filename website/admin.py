from django.contrib import admin
from django.utils.html import format_html

from .models import Record, Contact, Account, Lead, Deal, Product, Requisition, Branch, IncomePayment, PaymentPurpose

# from django.contrib.auth.admin import UserAdmin

# Change the title and header
admin.site.site_header = "BunyodkorERP Platform"
admin.site.site_title = "BunyodkorERP Platform"
admin.site.index_title = "BunyodkorERP Platform | created by TEAMS"


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = [ 'first_name', 'last_name', 'thumbnail', 'email', 'birthday', 'phone', 'country', 'state', 'city', 'id']
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('email', 'sex', 'country', 'state', 'city')

    def thumbnail(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width: 50px; height:50px;" />', obj.avatar.url)
        return ""

    thumbnail.short_description = 'Avatar'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'thumbnail', 'email', 'company', 'lead_status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company__account_name')
    list_filter = ('lead_status', 'industry', 'account_manager', 'created_at')
    # date_hierarchy = 'created_at'

    # Make 'created_by' read-only so it cannot be manually edited
    readonly_fields = ['created_by', 'created_at']

    # Automatically assign 'created_by' to the current user on save
    def save_model(self, request, obj, form, change):
        if not change:  # If it's a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def thumbnail(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width: 50px; height:50px;" />', obj.profile_picture.url)
        return ""

    thumbnail.short_description = 'Avatar'



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


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'deal_type', 'deal_stage', 'amount', 'currency', 'start_date', 'close_date', 'deal_status')
    list_filter = ('deal_type', 'deal_stage', 'deal_status', 'currency')
    search_fields = ('name', 'account__account_name', 'contact__first_name', 'contact__last_name')
    date_hierarchy = 'close_date'
    ordering = ('-close_date',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumbnail', 'category', 'price', 'quantity_in_stock', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('category',)

    def thumbnail(self, obj):
        if obj.product_picture:
            return format_html('<img src="{}" style="width: 50px; height:50px;" />', obj.product_picture.url)
        return ""

    thumbnail.short_description = 'Picture'


@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    list_display = (
        'product_name', 'product_model', 'quantity', 'unit_of_measure',
        'created_by', 'created_at',
        'director_status', 'supply_status', 'finance_status', 'leader_status',  'warehouse_status'
    )
    list_filter = (
        'unit_of_measure', 'created_at',
        'director_status', 'supply_status', 'finance_status', 'leader_status', 'warehouse_status'
    )
    search_fields = ('product_name', 'product_model', 'created_by__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'created_by')

    fieldsets = (
        ('Mahsulot haqida ma’lumot', {
            'fields': (
                'product_image', 'product_name', 'product_model',
                'usage_location', 'usage_object', 'unit_of_measure', 'quantity'
            )
        }),
        ('Narx va Takliflar', {
            'fields': (
                'previous_price', 'offer_prices1', 'offer_prices2', 'other_offers'
            )
        }),
        ('Tastiqlar', {
            'fields': (
                'director_status', 'supply_status', 'finance_status', 'leader_status', 'warehouse_status'
            )
        }),
        ('Yaratilgan', {
            'fields': ('created_by', 'created_at')
        }),
    )

    # Automatically assign 'created_by' to the current user on save
    def save_model(self, request, obj, form, change):
        if not change:  # If it's a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "address")  # o‘zingizdagi fieldlarni yozing

@admin.register(PaymentPurpose)
class PaymentPurposeAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")  # o‘zingizdagi fieldlarni yozing


@admin.register(IncomePayment)
class IncomePaymentAdmin(admin.ModelAdmin):
    list_display = (
        'created_by',
        'created_at',
        'payment_date',
        'company_name',
        'inn',
        'currency',
        'amount',
        'payment_purpose',
        'bank_payment_purpose',
        'our_branch',
        'account_number',
        'exchange_rate',
        'amount_in_uzs',
    )
    list_filter = ('currency', 'payment_purpose', 'our_branch', 'payment_date')
    search_fields = ('company_name', 'inn')