from django import forms
from .models import Record, Product
from .models import Contact


class AddRecordForm(forms.ModelForm):
	class Meta:
		model = Record
		fields = [
			'first_name', 'last_name', 'father_name', 'birthday', 'nationality',
			'zipcode', 'address', 'city', 'state', 'country',
			'email', 'phone', 'sex', 'family_situation', 'avatar',
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
			'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'})
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



class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = '__all__'
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control'}),
			'email': forms.EmailInput(attrs={'class': 'form-control'}),
			'phone_mobile': forms.TextInput(attrs={'class': 'form-control'}),
			'company_name': forms.TextInput(attrs={'class': 'form-control'}),
			'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
		}
		exclude = ['created_by']  # Exclude 'created_by' from the form


