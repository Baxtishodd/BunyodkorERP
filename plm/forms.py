from django import forms
from .models import ProductModel, Employee, Order, WorkType, FabricArrival, Accessory



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
        fields = ['client', 'artikul', 'quantity', 'rangi', 'deadline', 'model_picture']
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mijoz nomi'}),
            'artikul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artikul'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Miqdor'}),
            'rangi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rang'}),
            'model_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
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
        fields = ['order', 'fabric_name', 'measure_value', 'measure_unit', 'gramaj', 'arrival_date', 'factory_name']
        widgets = {
            'order': forms.Select(attrs={'class': 'form-select'}),
            'fabric_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mato nomi'}),
            'measure_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Miqdori'}),
            'measure_unit': forms.Select(attrs={'class': 'form-select'}),
            'gramaj': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Gramaj'}),
            'arrival_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'factory_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fabrika nomi'}),
        }
        labels = {
            'order': 'Buyurtma',
            'fabric_name': 'Mato nomi',
            'measure_value': 'Miqdori',
            'measure_unit': 'O‘lchov birligi',
            'gramaj': 'Gramaj',
            'arrival_date': 'Kelgan sana',
            'factory_name': 'Fabrika',
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




















