from django import forms
from .models import (ProductModel, Employee, Order, WorkType, FabricArrival, Accessory, Cutting, Printing, OrderSize,
                     Stitching, Ironing)



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
        fields = ['client', 'artikul','rangi', 'deadline', 'model_picture']
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mijoz nomi'}),
            'artikul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artikul'}),
            'rangi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rang'}),
            'model_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
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


























