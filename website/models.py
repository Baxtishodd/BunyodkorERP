from django.db import models


class Record(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)

	def __str__(self):
		return f"{self.first_name} {self.last_name}"


class Product(models.Model):
	created_at = models.DateTimeField(auto_now=True)
	customer_name = models.CharField(max_length=100)# mijoz nomi
	model_id = models.CharField(max_length=100)		# model idsi
	model_sign_date = models.DateTimeField()		# model imzolangan sana
	model_FI_date = models.DateTimeField()			# model FI sana
	quantity = models.IntegerField() 				# model soni
	example_LD = models.CharField(max_length=100)
	example_FIT = models.CharField(max_length=100)
	example_BULK = models.CharField(max_length=100)
	example_Print = models.CharField(max_length=100)
	example_PPS = models.CharField(max_length=100)
	slice_qty = models.IntegerField()
	slice_status = models.CharField(max_length=50) 	# kesim statusi
	print_qty = models.IntegerField()
	print_status = models.CharField(max_length=50)	# bo`yoq pechat statusi
	sewing_qty = models.IntegerField()
	sewing_status = models.CharField(max_length=50)	# tikim statusi
	packing_qty = models.IntegerField()
	packing_status = models.CharField(max_length=50)# qadoqlangan korobka statusi
	date_of_update = models.CharField(max_length=50)


	def __str__(self):
		return f"{self.customer_name}"

