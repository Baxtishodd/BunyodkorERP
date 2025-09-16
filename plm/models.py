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



class ProductionLine(models.Model):
    name = models.CharField(max_length=100, verbose_name="Patok nomi")

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=200, verbose_name="Buyurtma nomi")
    quantity = models.PositiveIntegerField(verbose_name="Miqdori (dona)")
    line = models.ForeignKey(
        ProductionLine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Patok",
        default="Tanlang"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} dona)"


class Employee(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Ism familiya")
    line = models.ForeignKey(ProductionLine, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name


class WorkType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ish turi")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (so‘m/dona)")

    def __str__(self):
        return f"{self.name} ({self.price} so‘m)"


class HourlyWork(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="hourly_works")
    line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE, null=True, blank=True)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="hourly_works")

    date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(verbose_name="Boshlanish vaqti")   # masalan 08:00
    end_time = models.TimeField(verbose_name="Tugash vaqti")         # masalan 09:00
    quantity = models.PositiveIntegerField(verbose_name="Qilingan ish soni")

    @property
    def total_amount(self):
        return self.quantity * self.work_type.price

    def __str__(self):
        return f"{self.employee.full_name} | {self.work_type.name} | {self.start_time}-{self.end_time}"