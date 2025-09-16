from django import forms
from .models import ProductModel, Employee

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





