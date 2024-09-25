from django.contrib import admin
from .models import Record, Product
from django.contrib.auth.admin import UserAdmin


class RecordAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'birthday', 'phone', 'sex', 'country', 'state', 'city', 'id']
    search_fields = ('first_name', 'last_name', 'email', 'phone')


admin.site.register(Record, RecordAdmin)
admin.site.register(Product)

