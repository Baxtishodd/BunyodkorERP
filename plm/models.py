from django.db import models
from django.conf import settings


class ProductModel(models.Model):
    artikul = models.CharField(max_length=100, verbose_name="Artikul", blank=True, null=True,)
    mijoz = models.CharField(max_length=200, verbose_name="Mijoz")
    ish_soni = models.PositiveIntegerField(verbose_name="Ish soni", default=0)
    bajarilgan = models.PositiveIntegerField(verbose_name="Bajarilgan", default=0, blank=True, null=True,)

    # Ish jarayonlari (raqamli ko‘rsatkich)
    kesim = models.PositiveIntegerField(verbose_name="Kesim soni", blank=True, null=True,)
    dazmol = models.PositiveIntegerField(verbose_name="Dazmol soni", blank=True, null=True,)
    pechat = models.PositiveIntegerField(verbose_name="Pechat soni", blank=True, null=True,)
    sifat_nazorati = models.PositiveIntegerField(verbose_name="Sifat nazorati soni", blank=True, null=True,)
    tasnif = models.PositiveIntegerField( verbose_name="Tasnif soni", blank=True, null=True,)
    qadoq = models.PositiveIntegerField(verbose_name="Qadoq soni", blank=True, null=True,)
    tikim = models.PositiveIntegerField( verbose_name="Tikim soni", blank=True, null=True,)

    # Model rasmi
    model_picture = models.ImageField(upload_to="models/", blank=True, null=True, verbose_name="Model rasmi")

    # Kim tomonidan yaratilgani
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Yaratgan foydalanuvchi"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    def __str__(self):
        return f"{self.artikul} - {self.mijoz}"
