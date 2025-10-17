from django.db import models
from django.conf import settings

SIZE_CHOICES = [
        ('oversize', 'Oversize'),
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
        ('4XL', '4XL'),
        ('5XL', '5XL'),
        ('6XL', '6XL'),
        ('7XL', '7XL'),
        ('8XL', '8XL'),
        ('9XL', '9XL'),
        ('10XL', '10XL'),
        ('11XL', '11XL'),
        ('12XL', '12XL'),
        ('40', '40'),
        ('42', '42'),
        ('44', '44'),
        ('46', '46'),
        ('48', '48'),
        ('50', '50'),
        ('52', '52'),
        ('54', '54'),
        ('56', '56'),
        ('58', '58'),
        ('60', '60'),
        ('62', '62'),
        ('64', '64'),
        ('66', '66'),
        ('68', '68'),
        ('70', '70'),
        ('42-44','42-44'),
        ('46-48','46-48'),
        ('50-52','50-52'),
        ('54-56','54-56'),
        ('58-60','58-60'),
        ('62-64','62-64'),
        ('66-68','66-68'),
        ('70-72','70-72'),
    ]

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


class Order(models.Model):
    client = models.CharField(max_length=200, verbose_name="Mijoz nomi", blank=True, null=True)
    artikul = models.CharField(max_length=100, verbose_name="Artikuli", blank=True, null=True,)
    rangi = models.CharField(max_length=100, verbose_name="Rangi", blank=True, null=True, )

    deadline = models.DateTimeField(blank=True, null=True, verbose_name="Yuklanish vaqti")
    # Model rasmi
    model_picture = models.ImageField(upload_to="orders/", blank=True, null=True, verbose_name="Model rasmi")

    # Kim tomonidan yaratilgani
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Yaratgan foydalanuvchi"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    def __str__(self):
        client_name = self.client if self.client else "Noma'lum mijoz"
        artikul_name = self.artikul if self.artikul else "Artikul yo‘q"
        return f"{client_name} - {artikul_name} ({self.sum_order_size()} dona)"

    def sum_order_size(self):
        return sum(c.quantity or 0 for c in self.ordersize.all())


class OrderSize(models.Model):
    SIZE_CHOICES = [
        ('oversize', 'Oversize'),
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
        ('4XL', '4XL'),
        ('5XL', '5XL'),
        ('6XL', '6XL'),
        ('7XL', '7XL'),
        ('8XL', '8XL'),
        ('9XL', '9XL'),
        ('10XL', '10XL'),
        ('11XL', '11XL'),
        ('12XL', '12XL'),
        ('40', '40'),
        ('42', '42'),
        ('44', '44'),
        ('46', '46'),
        ('48', '48'),
        ('50', '50'),
        ('52', '52'),
        ('54', '54'),
        ('56', '56'),
        ('58', '58'),
        ('60', '60'),
        ('62', '62'),
        ('64', '64'),
        ('66', '66'),
        ('68', '68'),
        ('70', '70'),
        ('42-44','42-44'),
        ('46-48','46-48'),
        ('50-52','50-52'),
        ('54-56','54-56'),
        ('58-60','58-60'),
        ('62-64','62-64'),
        ('66-68','66-68'),
        ('70-72','70-72'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="ordersize", verbose_name="Buyurtma")
    quantity = models.PositiveIntegerField(verbose_name="Soni")
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default="oversize", verbose_name="O‘lchami")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Muallif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    def __str__(self):
        return f"{self.order} - {self.quantity}-{self.size}"


class ProductionLine(models.Model):
    name = models.CharField(max_length=100, verbose_name="Patok nomi")

    def __str__(self):
        return self.name

    # Hodimlar sonini hisoblash
    def employee_count(self):
        return self.employee_set.count()

    # Normani olish (so‘nggi qo‘shilgan norma)
    def current_norm(self):
        return self.norm_set.last()


class ModelAssigned(models.Model):
    line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)
    model_name = models.ForeignKey("Order", on_delete=models.CASCADE, verbose_name="Buyurtma (Artikul)")
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_name} ({self.line.name})"


class Norm(models.Model):
    line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)
    daily_norm = models.PositiveIntegerField(verbose_name="Kunlik norma (dona)")
    hourly_norm = models.PositiveIntegerField(verbose_name="Soatlik norma (dona)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.line.name} - {self.daily_norm} dona/kun"


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


class FabricArrival(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="fabric_arrival", verbose_name="Qaysi buyurtma uchun")
    fabric_name = models.CharField(max_length=200, verbose_name="Mato nomi")
    measure_value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Miqdori",  null=True, blank=True)  # yangi qo‘shildi
    measure_unit = models.CharField(
        max_length=10,
        choices=[('kg', 'Kilogram'), ('m', 'Metr')], default='kg',
        verbose_name="O‘lchov birligi",  null=True, blank=True
    )
    gramaj = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Gramaj", null=True, blank=True,)
    arrival_date = models.DateTimeField(verbose_name="Qachon kelganligi")
    factory_name = models.CharField(max_length=200, verbose_name="Qaysi fabrikadan kelganligi")
    is_confirmed = models.BooleanField(default=False, verbose_name="Tasdiqlandi")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Muallif")
    created_at = models.DateTimeField(auto_now_add=True,  null=True, blank=True,)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti",  null=True, blank=True,)

    def __str__(self):
        return f"{self.fabric_name} → {self.order}"


class Accessory(models.Model):
    UNIT_CHOICES = [
        ('dona', 'Dona'),
        ('kg', 'Kg'),
        ('metr', 'Metr'),
        ('pachka', 'Pachka'),
        ('paket', 'Paket'),
        ('quti', 'Quti'),
        ('litr', 'Litr'),
    ]

    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="accessories", verbose_name="Buyurtma")
    name = models.CharField(max_length=200, verbose_name="Aksessuar nomi")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Soni")
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='dona', verbose_name="Birligi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


class Cutting(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="cuttings", verbose_name="Buyurtma")
    pastal_soni = models.PositiveIntegerField(verbose_name="Pastal soni")
    pastal_olchami = models.CharField(max_length=20, choices=SIZE_CHOICES, default="oversize", verbose_name="Pastal o‘lchami")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Muallif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    def __str__(self):
        return f"{self.order} - {self.pastal_soni} dona ({self.pastal_olchami})"


class Printing(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="prints", verbose_name="Buyurtma")
    quantity = models.PositiveIntegerField(verbose_name="Soni")
    daily_work_date = models.DateField(verbose_name="Kunlik bosilgan pechat")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Muallif")

    def __str__(self):
        return f"{self.order} modeli  ({self.quantity}) dona pechat ishi"


class Stitching(models.Model):
    STATUS_CHOICES = [
        ("pending", "Boshlanmagan"),
        ("in_progress", "Davom etmoqda"),
        ("done", "Tugallangan"),
    ]
    ordersize = models.ForeignKey("OrderSize", models.PROTECT, related_name="stitchings")
    quantity = models.PositiveIntegerField()   # tikilgan soni
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")  # ✅ Qo‘shildi
    date =  models.DateField(verbose_name="Kunlik tikim sanasi")

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.ordersize.order} - {self.ordersize.size} - {self.quantity} dona"


class Ironing(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="ironing", verbose_name="Buyurtma")
    quantity = models.PositiveIntegerField(verbose_name="Soni")
    daily_work_date = models.DateField(verbose_name="Kunlik dazmol ish sanasi")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Muallif")

    def __str__(self):
        return f"{self.order} modeli  ({self.quantity}) dona dazmol ishi"


class Inspection(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="inspections")

    total_checked = models.PositiveIntegerField(help_text="Umumiy tekshirilgan mahsulotlar soni")
    passed_quantity = models.PositiveIntegerField(default=0, help_text="Sifatdan o‘tgan mahsulotlar soni")
    failed_quantity = models.PositiveIntegerField(default=0, help_text="Sifatdan o‘tmagan mahsulotlar soni")

    defect_notes = models.TextField(blank=True, help_text="Nuqson haqida qisqacha izoh (agar bo‘lsa)")
    inspected_date = models.DateField(verbose_name="Kunlik Sifat nazorat ishi sanasi")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name="inspections", verbose_name="Muallif")

    class Meta:
        verbose_name = "Inspection"
        verbose_name_plural = "Inspections"
        ordering = ["-inspected_date"]

    def __str__(self):
        return f"{self.order} | {self.passed_quantity} ta o‘tgan"

    @property
    def passed_percentage(self):
        """Necha foiz mahsulot sifatdan o‘tganini hisoblaydi."""
        if self.total_checked > 0:
            return round((self.passed_quantity / self.total_checked) * 100, 2)
        return 0


class Packing(models.Model):
    PACKING_TYPE_CHOICES = [
        ("karopka", "Karopka"),
        ("paket", "Paket"),
        ("xalta", "Xalta"),
    ]

    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="packings")
    packing_type = models.CharField(max_length=20, choices=PACKING_TYPE_CHOICES, default="karopka", verbose_name="Qadoq turi")
    product_quantity = models.PositiveIntegerField(verbose_name="Qadoqlangan mahsulot soni")
    box_quantity = models.PositiveIntegerField(verbose_name="Yopilgan karopkalar soni")
    packed_date = models.DateField(verbose_name="Qadoqlangan sana")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="packings")

    class Meta:
        verbose_name = "Packing"
        verbose_name_plural = "Packings"
        ordering = ["-packed_date"]

    def __str__(self):
        return f"{self.order} — {self.packing_type} ({self.product_quantity} dona)"





class Shipment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Kutilmoqda"),
        ("ready", "Yuklashga tayyor"),
        ("shipped", "Yuklab jo‘natildi"),
    ]

    PACKAGE_TYPES = [
        ("box", "Karopka"),
        ("bag", "Xalta"),
        ("packet", "Paket"),
        ("pallet", "Pallet"),
        ("other", "Boshqa"),
    ]

    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="shipments",
        verbose_name="Buyurtma"
    )
    shipment_date = models.DateField(verbose_name="Yuk chiqarish sanasi")
    destination = models.CharField(max_length=200, verbose_name="Manzil")
    truck_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mashina raqami")
    driver_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Haydovchi ismi")

    # Yangi maydonlar
    package_type = models.CharField(
        max_length=20,
        choices=PACKAGE_TYPES,
        default="box",
        verbose_name="Qadoq turi"
    )
    product_quantity = models.PositiveIntegerField(default=0, verbose_name="Yuk miqdori (dona)")
    box_quantity = models.PositiveIntegerField(default=0, verbose_name="Karopkalar soni")

    note = models.TextField(blank=True, null=True, verbose_name="Izoh")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Holati")

    # Fayl biriktirish
    attachment = models.FileField(
        upload_to="shipments/files/",
        blank=True,
        null=True,
        verbose_name="Biriktirilgan fayl (ixtiyoriy)"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Yaratgan foydalanuvchi"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-shipment_date"]
        verbose_name = "Yuklama"
        verbose_name_plural = "Yuklamalar"

    def __str__(self):
        return f"{self.order} - {self.destination} ({self.product_quantity} dona)"

    @property
    def is_due_soon(self):
        from datetime import date, timedelta
        return self.shipment_date <= date.today() + timedelta(days=2)


# models.py

class ShipmentInvoice(models.Model):
    STATUS_CHOICES = [
        ("pending", "Kutilmoqda"),
        ("ready", "Yuklashga tayyor"),
        ("shipped", "Yuklab jo‘natildi"),
    ]

    PACKAGE_TYPES = [
        ("box", "Karopka"),
        ("bag", "Xalta"),
        ("packet", "Paket"),
        ("pallet", "Pallet"),
        ("other", "Boshqa"),
    ]

    number = models.PositiveIntegerField(
        verbose_name="Yuk xati raqami", unique=True, blank=True, null=True
    )
    date = models.DateField(verbose_name="Yuk xati sanasi")
    shipment_date = models.DateField(verbose_name="Yuk chiqarish sanasi")
    destination = models.CharField(max_length=200, verbose_name="Manzil")

    driver_name = models.CharField(max_length=150, verbose_name="Haydovchi ismi", blank=True, null=True)
    vehicle_number = models.CharField(max_length=50, verbose_name="Mashina raqami", blank=True, null=True)

    package_type = models.CharField(
        max_length=20,
        choices=PACKAGE_TYPES,
        default="box",
        verbose_name="Qadoq turi"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Holati"
    )

    note = models.TextField(blank=True, null=True, verbose_name="Izoh")

    attachment = models.FileField(
        upload_to="shipments/files/",
        blank=True,
        null=True,
        verbose_name="Biriktirilgan fayl (ixtiyoriy)"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Yaratgan foydalanuvchi"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # Agar yangi yozuv bo‘lsa va number hali berilmagan bo‘lsa
        if not self.number:
            last_invoice = ShipmentInvoice.objects.order_by("-number").first()
            if last_invoice and last_invoice.number:
                self.number = last_invoice.number + 1
            else:
                self.number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Yuk xati №{self.number} ({self.get_status_display()})"



class ShipmentItem(models.Model):
    shipment = models.ForeignKey(ShipmentInvoice, on_delete=models.CASCADE, related_name="items")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Buyurtma")
    quantity = models.PositiveIntegerField(verbose_name="Yuk miqdori")
    unit = models.CharField(max_length=20, choices=[('dona', 'Dona'), ('kg', 'Kg'), ('karopka', 'Karopka')], default='dona')
    note = models.CharField(max_length=255, blank=True, null=True, verbose_name="Izoh")

    def __str__(self):
        return f"{self.order} → {self.quantity} {self.unit}"


# class Warehouse(models.Model):
#     name = models.CharField(max_length=150, verbose_name="Ombor nomi")
#     location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Manzil")
#     manager = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         verbose_name="Mas’ul shaxs"
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = "Ombor"
#         verbose_name_plural = "Omborlar"
#
#     def __str__(self):
#         return self.name
#
#
# class WarehouseItem(models.Model):
#     warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="items")
#     name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
#     category = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kategoriya (Tayyor kiyim, mato, ip, aksessuar...)")
#     quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Miqdor")
#     unit = models.CharField(
#         max_length=20,
#         choices=[
#             ('dona', 'Dona'),
#             ('kg', 'Kg'),
#             ('metr', 'Metr'),
#             ('pachka', 'Pachka'),
#             ('quti', 'Quti'),
#         ],
#         default='dona',
#         verbose_name="O‘lchov birligi"
#     )
#     last_updated = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"{self.name} ({self.quantity} {self.unit})"
#
#
# class WarehouseTransaction(models.Model):
#     TRANSACTION_TYPE = [
#         ('IN', 'Kirim'),
#         ('OUT', 'Chiqim'),
#     ]
#
#     warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
#     item = models.ForeignKey(WarehouseItem, on_delete=models.CASCADE)
#     transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE)
#     quantity = models.DecimalField(max_digits=12, decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True)
#     note = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.get_transaction_type_display()} - {self.item.name} ({self.quantity} {self.item.unit})"



































































