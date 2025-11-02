from django.contrib import admin

from .models import (ProductModel, Order, ProductionLine, Employee, WorkType, HourlyWork, Norm, ModelAssigned,
                     FabricArrival, Accessory, Cutting, Printing, OrderSize, Stitching, Ironing, Inspection,
                     Packing, ShipmentInvoice, ShipmentInvoice, ShipmentItem, Classification, ChangeLog)
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
    list_display = ("client", "artikul", "rangi", "status", "deadline", "created_by", "created_at", "updated_at")
    list_filter = ("status", "rangi", "deadline", "created_at")
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

    def total_stitched_display(self, obj):
        return obj.total_stitched()

    total_stitched_display.short_description = "Tikilgan son"

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


# @admin.register(Inspection)
# class InspectionAdmin(admin.ModelAdmin):
#     list_display = (
#         "order",
#         "total_checked",
#         "passed_quantity",
#         "failed_quantity",
#         "passed_percentage_display",
#         "inspected_date",
#         "created_by",
#     )
#     list_filter = ("inspected_date", "created_by")
#     search_fields = ("order__id", "order__name", "defect_notes")
#     readonly_fields = ("created_at", "updated_at", "passed_percentage_display")
#     date_hierarchy = "inspected_date"
#     ordering = ("-inspected_date",)
#
#     fieldsets = (
#         ("Buyurtma ma’lumoti", {
#             "fields": ("order", "created_by")
#         }),
#         ("Sifat nazorati", {
#             "fields": (
#                 "total_checked",
#                 "passed_quantity",
#                 "failed_quantity",
#                 "defect_notes",
#                 "passed_percentage_display",
#             )
#         }),
#         ("Sana ma’lumotlari", {
#             "fields": ("inspected_date", "created_at", "updated_at")
#         }),
#     )
#
#     @admin.display(description="O‘tgan %")
#     def passed_percentage_display(self, obj):
#         return f"{obj.passed_percentage} %"

# @admin.register(Inspection)
# class InspectionAdmin(admin.ModelAdmin):
#     list_display = (
#         "order",
#         "ordersize",
#         "checked_quantity",
#         "passed_quantity",
#         "failed_quantity",
#         "inspection_date",
#         "created_by",
#     )
#     list_filter = ("inspection_date", "created_by")
#     search_fields = ("order__client", "order__artikul", "ordersize__size")
#     date_hierarchy = "inspection_date"
#     ordering = ("-inspection_date",)



@admin.register(Packing)
class PackingAdmin(admin.ModelAdmin):
    list_display = ("order", "packing_type", "product_quantity", "box_quantity", "packed_date", "created_by")
    list_filter = ("packing_type", "packed_date")
    search_fields = ("order__client", "order__artikul")
    ordering = ("-packed_date",)



class ShipmentItemInline(admin.TabularInline):
    model = ShipmentItem
    extra = 1
    fields = ("order", "quantity", "unit", "package_type", "note")
    autocomplete_fields = ("order",)
    verbose_name = "Yuk tarkibi"
    verbose_name_plural = "Yuk tarkibi (Buyurtmalar)"
    min_num = 0


@admin.register(ShipmentInvoice)
class ShipmentInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "shipment_number",
        "shipment_date",
        "destination",
        "driver_name",
        "vehicle_number",
        "status",
        "item_count",
        "created_by",
        "created_at",
    )
    list_filter = ("status", "shipment_date", "created_at")
    search_fields = (
        "shipment_number",
        "destination",
        "driver_name",
        "vehicle_number",
    )
    ordering = ("-created_at",)
    readonly_fields = ("shipment_number", "created_at", "created_by")
    inlines = [ShipmentItemInline]  # 👈 Yuk xati ichida itemlar ko‘rinadi

    fieldsets = (
        ("Asosiy ma’lumotlar", {
            "fields": (
                "shipment_number",
                "shipment_date",
                "destination",
                "status",
                "note",
            ),
        }),
        ("Transport ma’lumotlari", {
            "fields": (
                "driver_name",
                "vehicle_number",
            ),
        }),
        ("Qo‘shimcha ma’lumotlar", {
            "fields": (
                "attachment",
                "created_by",
                "created_at",
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Yaratganda avtomatik foydalanuvchini belgilaydi"""
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ShipmentItem)
class ShipmentItemAdmin(admin.ModelAdmin):
    list_display = ("shipment", "order", "quantity", "unit", "package_type",   "note")
    list_filter = ("package_type", "unit")
    search_fields = ("shipment__shipment_number", "order__artikul", "order__client")
    autocomplete_fields = ("shipment", "order")


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = (
        "get_order",
        "get_artikul",
        "get_size",
        "first_sort",
        "second_sort",
        "defect",
        "total_classified_display",
        "classified_date",
        "created_by",
    )
    list_filter = ("classified_date", "created_by")
    search_fields = (
        "ordersize__order__client",
        "ordersize__order__artikul",
        "ordersize__size",
    )
    ordering = ("-classified_date",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            "fields": (
                "ordersize",
                "first_sort",
                "second_sort",
                "defect",
                "classified_date",
            )
        }),
        ("Tizim ma'lumotlari", {
            "fields": (
                "created_by",
                "created_at",
                "updated_at",
            )
        }),
    )

    # Buyurtma nomini chiqarish
    @admin.display(description="Buyurtma")
    def get_order(self, obj):
        return obj.ordersize.order.client if obj.ordersize and obj.ordersize.order else "-"

    # Artikulni chiqarish
    @admin.display(description="Artikul")
    def get_artikul(self, obj):
        return obj.ordersize.order.artikul if obj.ordersize and obj.ordersize.order else "-"

    # Razmerni chiqarish
    @admin.display(description="Razmer")
    def get_size(self, obj):
        return obj.ordersize.size if obj.ordersize else "-"

    # Jami tasnifni chiqarish
    @admin.display(description="Jami")
    def total_classified_display(self, obj):
        return obj.total_classified

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "ordersize",
        "passed_quantity",
        "failed_quantity",
        "total_checked",
        "inspection_date",
        "created_by",
    )
    list_filter = ("inspection_date", "created_by")
    search_fields = ("order__client", "ordersize__size")
    ordering = ("-inspection_date",)

    @admin.display(description="Jami tekshirilgan")
    def total_checked(self, obj):
        return obj.total_checked


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ("title", "version", "author", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("title", "description", "version")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            "fields": ("title", "version", "description")
        }),
        ("Qo‘shimcha", {
            "fields": ("author", "created_at"),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("author")

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)





































admin.site.register(ProductionLine, ProductionLineAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(WorkType, WorkTypeAdmin)
admin.site.register(HourlyWork, HourlyWorkAdmin)
