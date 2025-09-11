from django.contrib import admin

from .models import ProductModel
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