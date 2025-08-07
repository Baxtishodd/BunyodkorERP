from django import forms
from .models import Record, Contact, Account, Requisition # Product



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
# class Add_Product_Form(forms.ModelForm):
# 	STATUS_CHOICES = [
# 		('completed', 'Bajarilgan'),
# 		('pending', 'Boshlanmagan'),
# 		('in_progress', 'Jarayonda'),
# 	]
#
# 	customer_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Mijoz nomi", "class":"form-control"}), label="Mijoz nomi")
# 	model_id = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Model ID", "class":"form-control"}), label="")
# 	model_sign_date = forms.CharField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder":"Model imzolangan sana", "class":"form-control"}), label="")
# 	fi_date = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"FI Sana", "class":"form-control"}), label="")
# 	quantity = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Soni", "class":"form-control"}), label="")
# 	example_ld = forms.CharField( widget=forms.widgets.TextInput(attrs={"placeholder":"LD", "class":"form-control"}), label="")
# 	example_fit = forms.CharField( widget=forms.widgets.TextInput(attrs={"placeholder":"FIT", "class":"form-control"}), label="")
# 	example_bulk = forms.CharField( widget=forms.widgets.TextInput(attrs={"placeholder":"BULK", "class":"form-control"}), label="")
# 	example_print = forms.CharField( widget=forms.widgets.TextInput(attrs={"placeholder":"Print", "class":"form-control"}), label="")
# 	pps = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"PPS", "class":"form-control"}), label="")
# 	slice_qty = forms.IntegerField(widget=forms.widgets.TextInput(attrs={"placeholder": "Kesim soni", "class": "form-control"}), label="")
# 	slice_status = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"Kesim Statusi", "class":"form-control"}), label="")
# 	print_qty = forms.IntegerField(widget=forms.widgets.TextInput(attrs={"placeholder": "Pechat soni", "class": "form-control"}), label="")
# 	print_status = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"Pechat statusi", "class":"form-control"}), label="")
# 	sewing_qty = forms.IntegerField(widget=forms.widgets.TextInput(attrs={"placeholder": "Tikim soni", "class": "form-control"}), label="")
# 	sewing_status = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"Tikim statusi", "class":"form-control"}), label="")
# 	packing_qty = forms.IntegerField(widget=forms.widgets.TextInput(attrs={"placeholder": "Qadoqlash soni", "class": "form-control"}), label="")
# 	packing_status = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"Qadoqlash statusi", "class":"form-control"}), label="")
# 	date_of_update = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Yangilangan sana", "class": "form-control"}), label="")
#
# 	status = forms.ChoiceField(
# 		choices=STATUS_CHOICES,
# 		widget=forms.Select(attrs={
# 			"class": "form-control"
# 		})
# 	)
#
# 	class Meta:
# 		model = Product
# 		exclude = ("user",)



class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = '__all__'
		widgets = {
			# 'first_name': forms.TextInput(attrs={'class': 'form-control'}),
			# 'last_name': forms.TextInput(attrs={'class': 'form-control'}),
			# 'email': forms.EmailInput(attrs={'class': 'form-control'}),
			# 'phone_mobile': forms.TextInput(attrs={'class': 'form-control'}),
			# 'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),

			'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
			'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
			'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
			'contact_source': forms.Select(attrs={'class': 'form-control'}),
			'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),

			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
			'phone_office': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Office Phone'}),
			'phone_mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Phone'}),
			'fax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fax Number'}),
			'preferred_communication': forms.Select(attrs={'class': 'form-control'}),

			'country': forms.Select(attrs={'class': 'form-control'}),
			'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 2}),

			'lead_status': forms.Select(attrs={'class': 'form-control'}),
			'account_manager': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Manager'}),
			'lead_source': forms.Select(attrs={'class': 'form-control'}),

			'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Industry'}),
			'company_size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Size'}),
			'budget_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Budget Range'}),
			'interests': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Interests', 'rows': 3}),
			'preferred_language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred Language'}),

			'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Notes', 'rows': 4}),
		}
		exclude = ['created_by']  # Exclude 'created_by' from the form


# class ContactForm(forms.ModelForm):
# 	class Meta:
# 		model = Contact
# 		fields = [
# 			'first_name', 'last_name', 'job_title', 'department', 'contact_source', 'profile_picture',
# 			'email', 'phone_office', 'phone_mobile', 'fax', 'preferred_communication', 'country',
# 			'address', 'lead_status', 'account_manager', 'lead_source', 'industry', 'company_size',
# 			'budget_range', 'interests', 'preferred_language', 'birthday', 'notes'
# 		]
# 		widgets = {
# 			'lead_status': forms.Select(attrs={'class': 'form-control'}),
# 			'account_manager': forms.TextInput(attrs={'class': 'form-control'}),
# 			'lead_source': forms.Select(attrs={'class': 'form-control'}),
# 			'contact_source': forms.Select(attrs={'class': 'form-control'}),
# 			'country': forms.Select(attrs={'class': 'form-control'}),
# 			'preferred_communication': forms.Select(attrs={'class': 'form-control'}),
# 			'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
# 			'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
# 		}


class AccountForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = [
			'account_name',
			'director',
			'industry',
			'website',
			'phone',
			'address',
			'description',
			'annual_revenue',
			'account_manager'
		]
		widgets = {
			'description': forms.Textarea(attrs={'rows': 3}),
			'address': forms.Textarea(attrs={'rows': 2}),
		}
		exclude = ['account_manager']  # Exclude 'account_manager' from the form


class RequisitionForm(forms.ModelForm):
	class Meta:
		model = Requisition
		fields = [
			'product_name', 'product_model', 'usage_location', 'usage_object',
			'unit_of_measure', 'quantity', 'product_image', 'previous_price',
			'offer_prices1', 'offer_prices2', 'other_offers', 'warehouse_status'
	]
		widgets = {
			'product_name': forms.TextInput(attrs={'class': 'form-control'}),
			'product_model': forms.TextInput(attrs={'class': 'form-control'}),
			'usage_object': forms.TextInput(attrs={'class': 'form-control'}),
			'quantity1': forms.TextInput(attrs={'class': 'form-control'}),
			'usage_location': forms.Select(choices=Requisition.USAGE_LOCATION, attrs={'class': 'form-select'}),
			'unit_of_measure': forms.Select(choices=Requisition.UNIT_CHOICES, attrs={'class': 'form-select'}),
			'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

			'quantity': forms.NumberInput(attrs={
				'class': 'form-control',
				'min': '1',
				'step': '1',
				'inputmode': 'numeric',  # Mobil qurilmalar uchun
			}),

		}