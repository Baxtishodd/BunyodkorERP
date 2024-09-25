from random import choices

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record, Product


# class SignUpForm(UserCreationForm):
# 	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
# 	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ism'}))
# 	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Familiya'}))
#
#
# 	class Meta:
# 		model = User
# 		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
#
#
# 	def __init__(self, *args, **kwargs):
# 		super(SignUpForm, self).__init__(*args, **kwargs)
#
# 		self.fields['username'].widget.attrs['class'] = 'form-control'
# 		self.fields['username'].widget.attrs['placeholder'] = 'Username'
# 		self.fields['username'].label = ''
# 		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Qabul qiladi 150 belgilar yoki kamroq. Harflar, raqamlar, va faqat @/./+/-/_ belgialar. </small></span>'
#
# 		self.fields['password1'].widget.attrs['class'] = 'form-control'
# 		self.fields['password1'].widget.attrs['placeholder'] = 'Parol'
# 		self.fields['password1'].label = ''
# 		self.fields['password1'].help_text = ('<ul class="form-text text-muted small">'
# 											  '<li>Sizning parol ma\'lumotlaringiz bilan bir hil bo\'lmasin!</li>'
# 											  '<li>Sizning parol 8 belgidan kam bo\'lmasin!</li>'
# 											  '<li>Sizning parol juda ham oddiy bo\'lmasligi lozim!</li>'
# 											  '<li>Sizning parol faqat raqamlardan tashkil topmasligi lozim!</li></ul>')
#
# 		self.fields['password2'].widget.attrs['class'] = 'form-control'
# 		self.fields['password2'].widget.attrs['placeholder'] = 'Parol takroran'
# 		self.fields['password2'].label = ''
# 		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Tastiqlash uchun. Parolni takroran yozing. </small></span>'


class AddRecordForm(forms.ModelForm):
	class Meta:
		model = Record
		fields = [
			'first_name', 'last_name', 'father_name', 'birthday', 'nationality',
			'zipcode', 'address', 'city', 'state', 'country',
			'email', 'phone', 'sex', 'family_situation'
		]
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control'}),
			'father_name': forms.TextInput(attrs={'class': 'form-control'}),
			'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			'nationality': forms.TextInput(attrs={'class': 'form-control'}),
			'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
			'address': forms.TextInput(attrs={'class': 'form-control'}),
			'city': forms.TextInput(attrs={'class': 'form-control'}),
			'state': forms.TextInput(attrs={'class': 'form-control'}),
			'country': forms.TextInput(attrs={'class': 'form-control'}),
			'email': forms.EmailInput(attrs={'class': 'form-control'}),
			'phone': forms.TextInput(attrs={'class': 'form-control'}),
			'sex': forms.RadioSelect(choices=Record.SEX_CHOICES), # RadioType
			'family_situation': forms.Select(choices=Record.FAMILY_SITUATION_CHOICES,
											 attrs={'class': 'form-select'}),  # Dropdown
		}



# Create Add Product Form
class Add_Product_Form(forms.ModelForm):
	STATUS_CHOICES = [
		('completed', 'Bajarilgan'),
		('pending', 'Boshlanmagan'),
		('in_progress', 'Jarayonda'),
	]

	customer_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Mijoz nomi", "class":"form-control"}), label="Mijoz nomi")
	model_id = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Model ID", "class":"form-control"}), label="")
	model_sign_date = forms.CharField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder":"Model imzolangan sana", "class":"form-control"}), label="")
	fi_date = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"FI Sana", "class":"form-control"}), label="")
	quantity = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Soni", "class":"form-control"}), label="")
	example_ld = forms.CharField( widget=forms.widgets.TextInput(attrs={"placeholder":"LD", "class":"form-control"}), label="")
	example_fit = forms.CharField( widget=forms.widgets.TextInput(attrs={"placeholder":"FIT", "class":"form-control"}), label="")
	example_bulk = forms.CharField( widget=forms.widgets.TextInput(attrs={"placeholder":"BULK", "class":"form-control"}), label="")
	example_print = forms.CharField( widget=forms.widgets.TextInput(attrs={"placeholder":"Print", "class":"form-control"}), label="")
	pps = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"PPS", "class":"form-control"}), label="")
	slice_qty = forms.IntegerField(widget=forms.widgets.TextInput(attrs={"placeholder": "Kesim soni", "class": "form-control"}), label="")
	slice_status = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"Kesim Statusi", "class":"form-control"}), label="")
	print_qty = forms.IntegerField(widget=forms.widgets.TextInput(attrs={"placeholder": "Pechat soni", "class": "form-control"}), label="")
	print_status = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"Pechat statusi", "class":"form-control"}), label="")
	sewing_qty = forms.IntegerField(widget=forms.widgets.TextInput(attrs={"placeholder": "Tikim soni", "class": "form-control"}), label="")
	sewing_status = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"Tikim statusi", "class":"form-control"}), label="")
	packing_qty = forms.IntegerField(widget=forms.widgets.TextInput(attrs={"placeholder": "Qadoqlash soni", "class": "form-control"}), label="")
	packing_status = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"Qadoqlash statusi", "class":"form-control"}), label="")
	date_of_update = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Yangilangan sana", "class": "form-control"}), label="")

	status = forms.ChoiceField(
		choices=STATUS_CHOICES,
		widget=forms.Select(attrs={
			"class": "form-control"
		})
	)

	class Meta:
		model = Product
		exclude = ("user",)

