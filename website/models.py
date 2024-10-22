import os
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

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
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
		null=True, blank=True, related_name='records_created')  # New field
	updated_at = models.DateTimeField(auto_now=True) # New field

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
	avatar = models.ImageField(upload_to='avatars/', default='avatars/default-avatar.jpg',) # New field

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

# Contacts
class Contact(models.Model):
	PREFERRED_COMMUNICATION_CHOICES = [
		('email', 'Email'),
		('phone', 'Phone Call'),
		('whatsapp', 'WhatsApp'),
		('telegram', 'Telegram'),
		('sms', 'SMS'),
		('video_call', 'Video Call (Zoom/Google Meet)'),
		('in_person', 'In-Person Meeting'),
		('linkedin', 'LinkedIn Messaging'),
		('fax', 'Fax'),
	]

	LEAD_STATUS_CHOICES = [
		('new_inquiry', 'New Inquiry'),
		('initial_contact', 'Initial Contact Made'),
		('sample_requested', 'Sample Requested'),
		('sample_sent', 'Sample Sent'),
		('quote_requested', 'Quotation Requested'),
		('quote_sent', 'Quotation Sent'),
		('negotiation', 'Negotiation/Follow-Up'),
		('awaiting_po', 'Awaiting Purchase Order'),
		('po_received', 'Purchase Order Received'),
		('production_started', 'Production Started'),
		('order_shipped', 'Order Shipped'),
		('deal_closed', 'Deal Closed'),
		('lost', 'Lost'),
		('on_hold', 'On Hold'),
	]

	contact_source_choices = [
		('website', 'Website'),
		('referral', 'Referral'),
		('email_campaign', 'Email Campaign'),
		('social_media', 'Social Media'),
		('trade_show', 'Trade Show'),
		('direct_call', 'Direct Call'),
		('partner', 'Partner'),
		('advertisement', 'Advertisement'),
		('other', 'Other'),
	]

	COUNTRY_CHOICES = [
		('UZ', 'Uzbekistan'),
		('RU', 'Russia'),
		('CN', 'China'),
		('TR', 'Turkey'),
		('US', 'United States'),
		('DE', 'Germany'),
		('IN', 'India'),
		('IT', 'Italy'),
		('JP', 'Japan'),
		('FR', 'France'),
		('GB', 'United Kingdom'),
		('CA', 'Canada'),
		('BR', 'Brazil'),
		('AU', 'Australia'),
		('KR', 'South Korea'),
		('SA', 'Saudi Arabia'),
		('AE', 'United Arab Emirates'),
		('ES', 'Spain'),
		('NL', 'Netherlands'),
		('SE', 'Sweden'),
		('MX', 'Mexico'),
		('CH', 'Switzerland'),
		('PL', 'Poland'),
		('NG', 'Nigeria'),
		('ID', 'Indonesia'),
		('ZA', 'South Africa'),
		('AR', 'Argentina'),
		('EG', 'Egypt'),
		('MY', 'Malaysia'),
		('PH', 'Philippines'),
		('SG', 'Singapore'),
		('VN', 'Vietnam'),
		('TH', 'Thailand'),
		('BD', 'Bangladesh'),
		('IR', 'Iran'),
		('IQ', 'Iraq'),
		('KZ', 'Kazakhstan'),
		('UA', 'Ukraine'),
		('PK', 'Pakistan'),
		('IL', 'Israel'),
		('GR', 'Greece'),
		('PT', 'Portugal'),
		('BE', 'Belgium'),
		('DK', 'Denmark'),
		('NO', 'Norway'),
		('FI', 'Finland'),
		('AT', 'Austria'),
		('HU', 'Hungary'),
		('CZ', 'Czech Republic'),
		('SK', 'Slovakia'),
		('NZ', 'New Zealand'),
		('CL', 'Chile'),
		('PE', 'Peru'),
		('CO', 'Colombia'),
		('OTHER', 'Other'),
	]

	LEAD_SOURCE_CHOICES = [
		('website', 'Website Inquiry'),
		('trade_show', 'Trade Shows/Exhibitions'),
		('referral', 'Referral'),
		('social_media', 'Social Media'),
		('email_campaign', 'Email Campaigns'),
		('cold_call', 'Cold Call/Direct Outreach'),
		('distributor', 'Distributor/Agent'),
		('online_marketplace', 'Online Marketplace'),
		('print_media', 'Print Media'),
		('word_of_mouth', 'Word of Mouth'),
		('previous_client', 'Previous Client'),
		('local_business', 'Local Business Network'),
		('partnership', 'Partnerships'),
		('phone_inquiry', 'Inbound Phone Inquiry'),
		('search_engine', 'Search Engine'),
	]

	created_at = models.DateTimeField(default=timezone.now, editable=False)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
		null=True, blank=True, related_name='contact_created')  # New field
	updated_at = models.DateTimeField(auto_now=True)

	# Basic Information
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	job_title = models.CharField(max_length=100, blank=True, null=True)

	company = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_set')

	department = models.CharField(max_length=100, blank=True, null=True)
	contact_source = models.CharField(
		max_length=20,
		choices=contact_source_choices,
		default='other'
	)
	profile_picture = models.ImageField(upload_to='contacts/', blank=True, null=True)

	# Contact Details
	email = models.EmailField()
	phone_office = models.CharField(max_length=20, blank=True, null=True)
	phone_mobile = models.CharField(max_length=20, blank=True, null=True)
	fax = models.CharField(max_length=15, blank=True, null=True)
	preferred_communication = models.CharField(max_length=50, choices=PREFERRED_COMMUNICATION_CHOICES, default='email')

	# Geographical Information
	country = models.CharField(
		max_length=5,
		choices=COUNTRY_CHOICES,
		default='UZ'  # Default set to Uzbekistan
	)
	address = models.CharField(max_length=255, blank=True, null=True)

	# Relationship Status
	lead_status = models.CharField(max_length=50, choices=LEAD_STATUS_CHOICES, default='new_inquiry')
	account_manager = models.CharField(max_length=100, blank=True, null=True)
	lead_source = models.CharField(max_length=20, choices=LEAD_SOURCE_CHOICES, default='website')

	# Demographics and Preferences
	industry = models.CharField(max_length=100, blank=True, null=True)
	company_size = models.CharField(max_length=50, blank=True, null=True)
	budget_range = models.CharField(max_length=50, blank=True, null=True)
	interests = models.TextField(blank=True, null=True)
	preferred_language = models.CharField(max_length=50, blank=True, null=True)
	birthday = models.DateField(blank=True, null=True)

	# Additional Notes
	notes = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.company})"

	class Meta:
		permissions = [
			("can_view_contact", "Can view contact details"),
		]


# Account
class Account(models.Model):

	INDUSTRY_CHOICES = [
		('textile_manufacturing', 'Textile Manufacturing'),
		('apparel_fashion', 'Apparel and Fashion'),
		('home_textiles', 'Home Textiles'),
		('industrial_textiles', 'Industrial Textiles'),
		('retail', 'Retail'),
		('wholesale', 'Wholesale'),
		('ecommerce', 'E-commerce'),
		('furniture', 'Furniture'),
		('interior_design', 'Interior Design'),
		('hospitality', 'Hospitality'),
		('healthcare', 'Healthcare'),
		('automotive', 'Automotive'),
		('agriculture', 'Agriculture'),
		('construction', 'Construction'),
		('sports_leisure', 'Sports and Leisure'),
		('government', 'Government/Public Sector'),
		('education', 'Education'),
		('non_profit', 'Non-profit/NGO'),
		('other', 'Other'),
	]

	account_name = models.CharField(max_length=100, unique=True)
	director = models.CharField(max_length=100, blank=True, null=True)
	industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='textile_manufacturing')
	website = models.URLField(blank=True, null=True)
	phone = models.CharField(max_length=20, blank=True, null=True)
	address = models.CharField(max_length=255, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
	contacts = models.ManyToManyField('Contact', related_name='accounts')

	account_manager = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='managed_accounts')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.account_name}"

	class Meta:
		ordering = ['-created_at']


# Leads
class Lead(models.Model):
	LEAD_STATUS_CHOICES = [
		('new_inquiry', 'New Inquiry'),
		('initial_contact', 'Initial Contact Made'),
		('sample_requested', 'Sample Requested'),
		('sample_sent', 'Sample Sent'),
		('quote_requested', 'Quotation Requested'),
		('quote_sent', 'Quotation Sent'),
		('negotiation', 'Negotiation/Follow-Up'),
		('awaiting_po', 'Awaiting Purchase Order'),
		('po_received', 'Purchase Order Received'),
		('production_started', 'Production Started'),
		('order_shipped', 'Order Shipped'),
		('deal_closed', 'Deal Closed'),
		('lost', 'Lost'),
		('on_hold', 'On Hold'),
	]

	LEAD_SOURCE_CHOICES = [
		('website', 'Website Inquiry'),
		('trade_show', 'Trade Shows/Exhibitions'),
		('referral', 'Referral'),
		('social_media', 'Social Media'),
		('email_campaign', 'Email Campaigns'),
		('cold_call', 'Cold Call/Direct Outreach'),
		('distributor', 'Distributor/Agent'),
		('online_marketplace', 'Online Marketplace'),
		('print_media', 'Print Media'),
		('word_of_mouth', 'Word of Mouth'),
		('previous_client', 'Previous Client'),
		('local_business', 'Local Business Network'),
		('partnership', 'Partnerships'),
		('phone_inquiry', 'Inbound Phone Inquiry'),
		('search_engine', 'Search Engine'),
	]

	lead_name = models.CharField(max_length=255)
	company_name = models.CharField(max_length=255, blank=True, null=True)
	email = models.EmailField()
	phone = models.CharField(max_length=20, blank=True, null=True)
	account_manager = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='leads'
	)
	status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='new')
	source = models.CharField(max_length=20, choices=LEAD_SOURCE_CHOICES, default='website')
	description = models.TextField(blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.lead_name} ({self.company_name})"

	class Meta:
		ordering = ['-created_at']
