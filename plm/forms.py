from django import forms
from .models import (ProductModel, Employee, Order, WorkType, FabricArrival, Accessory, Cutting, Printing, OrderSize,
                     Stitching, Ironing, Packing, Shipment, ShipmentInvoice, ShipmentItem, ModelAssigned,
                     Classification, Inspection, ProductionLine, ChangeLog)


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = [
            "artikul", "mijoz", "ish_soni", "bajarilgan",
            "kesim", "pechat", "tasnif", "tikim", "dazmol",
            "sifat_nazorati", "qadoq",
            "model_picture",
        ]
        widgets = {
            "artikul": forms.TextInput(attrs={"class": "form-control", "placeholder": "Artikul"}),
            "mijoz": forms.TextInput(attrs={"class": "form-control", "placeholder": "Mijoz"}),
            "ish_soni": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "bajarilgan": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "kesim": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "pechat": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "tasnif": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "tikim": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "dazmol": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "sifat_nazorati": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "qadoq": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "model_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'line']

        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ism familiya"}),
            "line": forms.Select(choices=Employee.line,
                                 attrs={'class': 'form-select'})
        }


class OrderForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = ['client', 'artikul', 'rangi', 'deadline', 'model_picture', 'status']
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mijoz nomi'}),
            'artikul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artikul'}),
            'rangi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rang'}),
            'model_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class OrderSizeForm(forms.ModelForm):
    class Meta:
        model = OrderSize
        fields = ['quantity', 'size']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
        }


class WorkTypeForm(forms.ModelForm):
    class Meta:
        model = WorkType
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class FabricArrivalForm(forms.ModelForm):
    class Meta:
        model = FabricArrival
        fields = ['fabric_name', 'measure_value', 'measure_unit', 'gramaj', 'arrival_date', 'factory_name']
        widgets = {
            'fabric_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mato nomi'}),
            'measure_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Miqdori'}),
            'measure_unit': forms.Select(attrs={'class': 'form-select'}),
            'gramaj': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Gramaj'}),
            'arrival_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'factory_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fabrika nomi'}),
        }


class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = ['name', 'quantity', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Aksessuar nomi'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Soni'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
        }


class CuttingForm(forms.ModelForm):
    class Meta:
        model = Cutting
        fields = ['pastal_soni', 'pastal_olchami']
        widgets = {
            'pastal_soni': forms.NumberInput(attrs={'class': 'form-control'}),
            'pastal_olchami': forms.Select(attrs={'class': 'form-select'}),
        }


class PrintForm(forms.ModelForm):
    class Meta:
        model = Printing
        fields = ['quantity', 'daily_work_date']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Soni'}),
            'daily_work_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

        }


class StitchingForm(forms.ModelForm):
    class Meta:
        model = Stitching
        fields = ["ordersize", "quantity", "date"]
        widgets = {
            'ordersize': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Miqdori'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

        }
        labels = {
            'ordersize': 'Buyurtma o‘lchami',
            'quantity': 'Miqdori',
            'date': 'Sana',
        }

    def __init__(self, *args, **kwargs):
        order = kwargs.pop("order", None)
        super().__init__(*args, **kwargs)

        # Agar order berilgan bo‘lsa, faqat shu orderga tegishli ordersizelarni chiqaramiz
        if order:
            self.fields["ordersize"].queryset = OrderSize.objects.filter(order=order)

        # # Sana kiritilayotganini ko‘rsatamiz
        # self.fields["date"].widget = forms.DateInput(attrs={"type": "date"})


class IroningForm(forms.ModelForm):
    class Meta:
        model = Ironing
        fields = ['quantity', 'daily_work_date']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Soni'}),
            'daily_work_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

        }


class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ["ordersize", "passed_quantity", "failed_quantity", "inspection_date", "comment"]
        widgets = {
            "ordersize": forms.Select(attrs={"class": "form-select"}),
            "passed_quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "failed_quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "inspection_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class PackingForm(forms.ModelForm):
    class Meta:
        model = Packing
        fields = ["packing_type", "product_quantity", "box_quantity", "packed_date"]
        widgets = {
            "packing_type": forms.Select(attrs={"class": "form-select"}),
            "product_quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Mahsulot soni"}),
            "box_quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Karopkalar soni"}),
            "packed_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
        labels = {
            "packing_type": "Qadoq turi",
            "product_quantity": "Qadoqlangan mahsulot soni",
            "box_quantity": "Yopilgan karopkalar soni",
            "packed_date": "Qadoqlangan sana",
        }


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            "shipment_date",
            "destination",
            "truck_number",
            "driver_name",
            "package_type",
            "product_quantity",
            "box_quantity",
            "note",
            "status",
            "attachment",
        ]
        widgets = {
            "shipment_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "destination": forms.TextInput(attrs={"class": "form-control"}),
            "truck_number": forms.TextInput(attrs={"class": "form-control"}),
            "driver_name": forms.TextInput(attrs={"class": "form-control"}),
            "package_type": forms.Select(attrs={"class": "form-select"}),
            "product_quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "box_quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "attachment": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class ShipmentInvoiceForm(forms.ModelForm):
    class Meta:
        model = ShipmentInvoice
        fields = [
            "shipment_number",
            "shipment_date",
            "destination",
            "driver_name",
            "vehicle_number",
            "status",
            "note",
            "attachment",
        ]
        widgets = {
            "shipment_number": forms.TextInput(attrs={
                "class": "form-control",
                "readonly": True,
                "placeholder": "Avtomatik raqam"
            }),
            "shipment_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "destination": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Yuk manzili"
            }),
            "driver_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Haydovchi ismi"
            }),
            "vehicle_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Mashina raqami (masalan, 30A123AB)"
            }),
            "status": forms.Select(attrs={
                "class": "form-select"
            }),
            "note": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Izoh (ixtiyoriy)"
            }),
            "attachment": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }
        labels = {
            "shipment_number": "Yuk xati raqami avtomatik yaratiladi",
            "shipment_date": "Yuk jo‘natiladigan sana",
            "destination": "Manzil",
            "driver_name": "Haydovchi ismi",
            "vehicle_number": "Mashina raqami",
            "status": "Holati",
            "note": "Izoh",
            "attachment": "Biriktirilgan fayl",
        }


class ShipmentItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentItem
        fields = [
            "order",
            "size",
            "quantity",
            "unit",
            "package_type",
            "note",
        ]
        widgets = {
            "order": forms.Select(attrs={"class": "form-select select2"}),
            "size": forms.Select(attrs={"class": "form-select"}),  # yangi qo‘shildi
            "quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Yuk miqdori"}),
            "unit": forms.Select(attrs={"class": "form-select"}),
            "package_type": forms.Select(attrs={"class": "form-select"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Izoh (ixtiyoriy)"}),
        }
        labels = {
            "order": "Buyurtma",
            "size": "O‘lchami",
            "quantity": "Yuk miqdori",
            "unit": "O‘lchov birligi",
            "package_type": "Qadoq turi",
            "note": "Izoh",
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # faqat ModelAssigned orqali tasdiqlangan buyurtmalarni ko‘rsatish
            confirmed_orders = Order.objects.filter(
                id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
            )
            self.fields['order'].queryset = confirmed_orders


class ClassificationForm(forms.ModelForm):
    class Meta:
        model = Classification
        fields = ["ordersize", "first_sort", "second_sort", "defect", "classified_date"]
        widgets = {
            "ordersize": forms.Select(attrs={"class": "form-select"}),
            "first_sort": forms.NumberInput(attrs={"class": "form-control", "placeholder": "1-sort soni"}),
            "second_sort": forms.NumberInput(attrs={"class": "form-control", "placeholder": "2-sort soni"}),
            "defect": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Brak soni"}),
            "classified_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
        labels = {
            "ordersize": "Buyurtma razmeri",
            "first_sort": "1-sort",
            "second_sort": "2-sort",
            "defect": "Brak",
            "classified_date": "Tasnif sanasi",
        }


class ModelAssignedForm(forms.ModelForm):
    class Meta:
        model = ModelAssigned
        fields = ["line", "model_name"]
        widgets = {
            "line": forms.Select(attrs={"class": "form-select"}),
            "model_name": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "line": "Patok",
            "model_name": "Buyurtma (Artikul)",
        }


class ProductionLineForm(forms.ModelForm):
    class Meta:
        model = ProductionLine
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patok nomi'}),
        }


class ChangeLogForm(forms.ModelForm):
    class Meta:
        model = ChangeLog
        fields = ["title", "description", "version"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "O‘zgarish nomi"}),
            "version": forms.TextInput(attrs={"class": "form-control", "placeholder": "v1.0.0"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Nimalar o‘zgardi?"}),
        }

















