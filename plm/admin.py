from django.contrib import admin

from .models import (ProductModel, Order, ProductionLine, Employee, WorkType, HourlyWork, Norm, ModelAssigned,
                     FabricArrival, Accessory, Cutting, Printing, OrderSize, Stitching, Ironing)
from django.utils.html import format_html


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id", "artikul", "mijoz", "ish_soni", "bajarilgan",
        "kesim", "tikim", "pechat", "dazmol",
        "sifat_nazorati", "tasnif", "qadoq", "created_by",
        "created_at", "updated_at"
    )
    list_filter = ("mijoz", "created_at")
    search_fields = ("artikul", "mijoz")
    readonly_fields = ("created_at", "updated_at", "created_by",)

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            "fields": ("artikul", "mijoz", "ish_soni", "bajarilgan", "model_picture")
        }),
        ("Ish jarayonlari", {
            "fields": ("kesim", "pechat", "tasnif", "tikim",  "dazmol", "sifat_nazorati",  "qadoq")
        }),
        ("Tizim ma'lumotlari", {
            "fields": ("created_at", "updated_at", "created_by",)
        }),
    )

    def image_preview(self, obj):
        if obj.model_picture:
            return format_html('<img src="{}" style="width:60px; height:auto; border-radius:5px;" />',
                               obj.model_picture.url)
        return "Rasm yo‘q"

    image_preview.short_description = "Model rasmi"


class ProductionLineInline(admin.TabularInline):
    model = ProductionLine
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("client", "artikul", "rangi", "deadline", "created_by", "created_at", "updated_at")
    list_filter = ("rangi", "deadline", "created_at")
    search_fields = ("client", "artikul", "rangi")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Buyurtma ma'lumotlari", {
            "fields": ("client", "artikul", "rangi", "deadline", "model_picture")
        }),
        ("Tizim ma'lumotlari", {
            "fields": ("created_by", "created_at", "updated_at"),
        }),
    )

@admin.register(OrderSize)
class OrderSizeAdmin(admin.ModelAdmin):
    list_display = ("order", "size", "quantity", "author", "created_at", "updated_at")
    list_filter = ("size", "created_at", "updated_at")
    search_fields = ("order__id", "size", "author__username")


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "line")
    search_fields = ("full_name",)
    list_filter = ("line",)


class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)


class HourlyWorkAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "work_type",
        "order",
        "date",
        "start_time",
        "end_time",
        "quantity",
        "total_amount_display",
    )
    list_filter = ("date", "work_type", "order")
    search_fields = ("employee__full_name",)

    def total_amount_display(self, obj):
        return f"{obj.total_amount:,.0f} so‘m"
    total_amount_display.short_description = "Jami summa"

class ProductionLineAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(ModelAssigned)
class ModelAssignedAdmin(admin.ModelAdmin):
    list_display = ("model_name", "line", "assigned_date")
    search_fields = ("model_name", "line__name")
    list_filter = ("line", "assigned_date")
    ordering = ("-assigned_date",)


@admin.register(Norm)
class NormAdmin(admin.ModelAdmin):
    list_display = ("line", "daily_norm", "hourly_norm", "created_at")
    search_fields = ("line__name",)
    list_filter = ("line", "created_at")
    ordering = ("-created_at",)


@admin.register(FabricArrival)
class FabricArrivalAdmin(admin.ModelAdmin):
    list_display = ("fabric_name", "order", "measure_value", "measure_unit", "gramaj", "arrival_date", "factory_name", "is_confirmed")
    list_filter = ("is_confirmed", "measure_unit", "arrival_date", "factory_name")
    search_fields = ("fabric_name", "factory_name", "order__id")
    ordering = ("-arrival_date",)
    list_editable = ("is_confirmed",)


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'quantity', 'unit', 'created_at')
    list_filter = ('unit', 'order')
    search_fields = ('name', 'order__account_name')


@admin.register(Cutting)
class CuttingAdmin(admin.ModelAdmin):
    list_display = ('order', 'pastal_soni', 'pastal_olchami', 'author', 'created_at', 'updated_at')
    list_filter = ('pastal_olchami', 'created_at', 'updated_at')
    search_fields = ('order__order_name', 'author__username')


@admin.register(Printing)
class PrintingAdmin(admin.ModelAdmin):
    list_display = ('order', 'quantity', 'daily_work_date', 'created_at', 'updated_at', 'created_by')
    list_filter = ('order', 'created_by')
    search_fields = ('order__order_name', 'order__account_name')


@admin.register(Stitching)
class StitchingAdmin(admin.ModelAdmin):
    list_display = ("ordersize", "quantity", "status", "date", "created_at", "updated_at")
    list_filter = ("status", "date", "created_at")
    search_fields = ("ordersize__order__client", "ordersize__order__artikul", "ordersize__size")
    ordering = ("-date", "-created_at")


@admin.register(Ironing)
class IroningAdmin(admin.ModelAdmin):
    list_display = ('order', 'quantity', 'daily_work_date', 'created_at', 'updated_at', 'created_by')
    list_filter = ('order', 'created_by')
    search_fields = ('order__order_name', 'order__account_name')





























admin.site.register(ProductionLine, ProductionLineAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(WorkType, WorkTypeAdmin)
admin.site.register(HourlyWork, HourlyWorkAdmin)
