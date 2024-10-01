import os
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model



# Xodimlarni ro`yhatga olish modeli
class Record(models.Model):
	SEX_CHOICES = [
		('Ayol', 'Ayol'),
		('Erkak', 'Erkak'),
	]
	FAMILY_SITUATION_CHOICES = [
		("Yolg'iz", "Yolg'iz"),
		('Oilali', 'Oilali'),
	]

	created_at = models.DateTimeField(auto_now_add=True)
	# created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # New field

	# Xodim ma`lumotlari
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	father_name =  models.CharField(null=True, blank=True, max_length=50)
	birthday =  models.DateField(null=True, blank=True)
	nationality =  models.CharField(max_length=100, null=True, blank=True)
	zipcode = models.CharField(max_length=20, null=True, blank=True)
	address =  models.CharField(max_length=100, null=True, blank=True)
	city =  models.CharField(max_length=50, null=True, blank=True)
	state =  models.CharField(max_length=50, null=True, blank=True)
	country = models.CharField(max_length=50, null=True, blank=True)
	email = models.CharField(max_length=50, null=True, blank=True)
	phone = models.CharField(max_length=50, null=True, blank=True)
	sex = models.CharField(max_length=10, choices=SEX_CHOICES, null=True, blank=True)  # Using choices
	family_situation = models.CharField(max_length=10, default="Yolg'iz", choices=FAMILY_SITUATION_CHOICES)  # Using choices

	# Avatar field
	avatar = models.ImageField(upload_to='avatars/', default='avatars/default-avatar.jpg',)


	def __str__(self):
		return f"{self.first_name} {self.last_name}"


DEFAULT_AVATAR = 'avatars/default-avatar.jpg'  # Constant for the default avatar

# Signal to delete image file when the record is deleted
@receiver(post_delete, sender=Record)
def auto_delete_image_on_delete(sender, instance, **kwargs):
	"""
    Deletes the image file from the filesystem when the record is deleted.
    """
	if instance.avatar and instance.avatar.name != DEFAULT_AVATAR:  # Use constant
		if os.path.isfile(instance.avatar.path):
			os.remove(instance.avatar.path)

# Signal to delete old image file when the avatar is updated
@receiver(pre_save, sender=Record)
def auto_delete_image_on_change(sender, instance, **kwargs):
	"""
	Deletes old image file from the filesystem when a record's image is updated with a new one.
	"""
	if not instance.pk:
		return False  # If the instance is new (no previous image), return early

	try:
		# Get the old avatar before the record is saved
		old_image = Record.objects.get(pk=instance.pk).avatar
	except Record.DoesNotExist:
		return False  # If no old image exists, skip deletion

	new_image = instance.avatar
	# If the old image is not the same as the new one and is not the default avatar, delete it
	if old_image and old_image != new_image and old_image.name != DEFAULT_AVATAR:  # Use constant
		if os.path.isfile(old_image.path):
			os.remove(old_image.path)


class Product(models.Model):
	created_at = models.DateTimeField(auto_now=True)
	customer_name = models.CharField(max_length=100)# mijoz nomi
	model_id = models.CharField(max_length=100)		# model idsi
	model_sign_date = models.DateTimeField(null=True, blank=True)		# model imzolangan sana
	model_FI_date = models.DateTimeField(null=True, blank=True)			# model FI sana
	quantity = models.IntegerField() 				# model soni
	example_LD = models.CharField(max_length=100, null=True, blank=True)
	example_FIT = models.CharField(max_length=100, null=True, blank=True)
	example_BULK = models.CharField(max_length=100, null=True, blank=True)
	example_Print = models.CharField(max_length=100, null=True, blank=True)
	example_PPS = models.CharField(max_length=100, null=True, blank=True)
	slice_qty = models.IntegerField(null=True, blank=True)
	slice_status = models.CharField(max_length=50, null=True, blank=True) 	# kesim statusi
	print_qty = models.IntegerField(null=True, blank=True)
	print_status = models.CharField(max_length=50,null=True, blank=True )	# bo`yoq pechat statusi
	sewing_qty = models.IntegerField(null=True, blank=True)
	sewing_status = models.CharField(max_length=50, null=True, blank=True)	# tikim statusi
	packing_qty = models.IntegerField(null=True, blank=True)
	packing_status = models.CharField(max_length=50, null=True, blank=True)# qadoqlangan korobka statusi
	date_of_update = models.CharField(max_length=50, null=True, blank=True )


	def __str__(self):
		return f"{self.customer_name}"

