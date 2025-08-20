import os
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

from random import randint

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


# class Product_status(models.Model):
# 	created_at = models.DateTimeField(auto_now=True)
# 	customer_name = models.CharField(max_length=100)# mijoz nomi
# 	model_id = models.CharField(max_length=100)		# model idsi
# 	model_sign_date = models.DateTimeField(null=True, blank=True)		# model imzolangan sana
# 	model_FI_date = models.DateTimeField(null=True, blank=True)			# model FI sana
# 	quantity = models.IntegerField() 				# model soni
# 	example_LD = models.CharField(max_length=100, null=True, blank=True)
# 	example_FIT = models.CharField(max_length=100, null=True, blank=True)
# 	example_BULK = models.CharField(max_length=100, null=True, blank=True)
# 	example_Print = models.CharField(max_length=100, null=True, blank=True)
# 	example_PPS = models.CharField(max_length=100, null=True, blank=True)
# 	slice_qty = models.IntegerField(null=True, blank=True)
# 	slice_status = models.CharField(max_length=50, null=True, blank=True) 	# kesim statusi
# 	print_qty = models.IntegerField(null=True, blank=True)
# 	print_status = models.CharField(max_length=50,null=True, blank=True )	# bo`yoq pechat statusi
# 	sewing_qty = models.IntegerField(null=True, blank=True)
# 	sewing_status = models.CharField(max_length=50, null=True, blank=True)	# tikim statusi
# 	packing_qty = models.IntegerField(null=True, blank=True)
# 	packing_status = models.CharField(max_length=50, null=True, blank=True)# qadoqlangan korobka statusi
# 	date_of_update = models.CharField(max_length=50, null=True, blank=True )
#
#
# 	def __str__(self):
# 		return f"{self.customer_name}"

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
		('new_request', 'New Request'),
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




class Product(models.Model):
	CATEGORY_CHOICES = [
		('not_selected', 'Not selected'),
		('fiber', 'Fiber'),
		('fabric', 'Fabric'),
		('yarn', 'Yarn'),
		('garment', 'Garment'),
		('service', 'Service'),
	]
	CURRENCY_CHOICES = [
		('USD', 'Dollar ($)'),
		('RUB', 'Ruble (₽)'),
		('EUR', 'Euro (€)'),
		('UZS', 'UZS (so‘m)'),
	]
	UNIT_CHOICES = [
		('kg', 'Kilogram'),
		('m', 'Meter'),
		('pcs', 'Pieces'),
		('roll', 'Roll'),
	]

	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='not_selected')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
	quantity_in_stock = models.DecimalField(max_digits=10, decimal_places=2)
	unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='pcs')  # Unit of measurement
	product_picture = models.ImageField(upload_to='product_pictures/', blank=True, null=True)  # Product picture field

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.name} ({self.unit})'


# Deals
class Deal(models.Model):
	DEAL_STATUS_CHOICES = [
		('open', 'Open'),
		('won', 'Closed Won'),
		('lost', 'Closed Lost'),
	]

	DEAL_STAGE_CHOICES = [
		('initial_contact', 'Initial Contact'),
		('sample_delivery', 'Sample Delivery'),
		('quotation_sent', 'Quotation Sent'),
		('negotiation', 'Negotiation'),
		('final_approval', 'Final Approval'),
		('order_processing', 'Order Processing'),
		('closed_won', 'Closed Won'),
		('closed_lost', 'Closed Lost'),
	]

	CURRENCY_CHOICES = [
		('USD', 'Dollar ($)'),
		('RUB', 'Ruble (₽)'),
		('EUR', 'Euro (€)'),
		('UZS', 'UZS (so‘m)'),
	]

	DEAL_TYPE_CHOICES = [
		('not_selected', 'Not selected'),
		('sale', 'Sale'),
		('sale_of_fiber', 'Sale of Fiber'),
		('sale_of_fabric', 'Sale of Fabric'),
		('sale_of_yarn', 'Sale of Yarn'),
		('sale_of_garment', 'Sale of Garment'),
		('sale_of_services', 'Sale of Services'),
	]

	DEAL_SOURCE_CHOICES = [
		('referral', 'Referral'),
		('cold_call', 'Cold Call'),
		('email_campaign', 'Email Campaign'),
		('website_inquiry', 'Website Inquiry'),
		('trade_show', 'Trade Show'),
		('online_advertisement', 'Online Advertisement'),
		('distributor', 'Distributor'),
		('social_media', 'Social Media'),
		('direct_visit', 'Direct Visit'),
	]

	account = models.ForeignKey('Account',  on_delete=models.SET_NULL, null=True, blank=True, related_name='deals')
	contact = models.ForeignKey('Contact', on_delete=models.CASCADE, null=True, blank=True, related_name='deals')
	products = models.ManyToManyField('Product', related_name='deals')  # Link to Product model
	name = models.CharField(max_length=255)

	deal_status = models.CharField(max_length=10, choices=DEAL_STATUS_CHOICES, default='open')
	deal_stage = models.CharField(max_length=20, choices=DEAL_STAGE_CHOICES, default='initial_contact')
	deal_type = models.CharField(max_length=20, choices=DEAL_TYPE_CHOICES, default='not_selected')
	source = models.CharField(max_length=20, choices=DEAL_SOURCE_CHOICES, default='website_inquiry')
	amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,)
	currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
	start_date = models.DateField()
	close_date = models.DateField()
	description = models.TextField(blank=True, null=True)
	account_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	""""
	Савдо бу’лди: 
	Nm50/1 
	BUNYODKOR - 60 тонн, 
	$2.20kg. 
	Харидор Красная Талка - ПрофиТекс ёки Ип Колесова;
	Юклама Галтекслан кегин;  
	Тулов 20 тонн 18 ОКТ гача; 
	колгани 25 ОКТ гача
	"""

	def __str__(self):
		return self.name

# Buyurtmanoma yaratish modeli Bo`lim boshliqlari yaratadi.
class Requisition(models.Model):

	UNIT_CHOICES = [
		('kg', 'Kilogram (kg)'),
		('g', 'Gram (g)'),
		('tonna', 'Tonna'),
		('l', 'Litr (l)'),
		('ml', 'Millilitr (ml)'),
		('dona', 'Dona'),
		('karopka', 'Karopka'),
		('metr', 'Metr'),
		('sm', 'Santimetr'),
		('rulon', 'Rulon'),
		('set', 'To‘plam (Set)'),
		('pachka', 'Pachka'),
		('quti', 'Quti'),
		('juft', 'Juft'),
		('list', 'List'),
		('bo‘lak', 'Bo‘lak'),
	]

	USAGE_LOCATION = [
		("koson_fashion","Koson Fashion MCHJ"),
		("bunyodkor", "Bunyodkor MCHJ"),
		("texnopark", "Bunyodkor Industrial Texnopark"),

	]

	# Direktorlar ro`yahti
	DIRECTOR_CHOICES = [
		# ('USERNAME', 'Fullname'),
		('Jamshidbek', 'Jamshidbek Saidaliev'),
		('Mujahid', 'Mujahid Iqbal'),
		('Pirnazarov', 'Pirnazarov Laziz'),
		('Saidaxror', 'Rakhimov Saidakhror'),
	]

	# Bo`lim boshliqlari zayavka yaratadi
	created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requisitions_created'
    )
	created_at = models.DateTimeField(auto_now_add=True)

	product_image = models.ImageField(upload_to='requisition_images/', null=True, blank=True)
	product_name = models.CharField(max_length=255)
	product_model = models.CharField(max_length=255, blank=True)
	usage_location = models.CharField(max_length=255, choices=USAGE_LOCATION, default='bunyodkor')
	usage_object = models.CharField(max_length=255, null=True, blank=True)

	unit_of_measure = models.CharField(
		max_length=20,
		choices=UNIT_CHOICES,
		default='dona',
		help_text="O‘lchov birligini tanlang"
	)
	quantity = models.PositiveIntegerField()

	#Ta`minot bo`limi tastiqlashi uchun
	previous_price = models.TextField(
		blank=True,
		help_text="Avvalgi xarid narxi va u bilan bog‘liq manba yoki joy haqida ma’lumot"
	)
	offer_prices1 = models.TextField(
		blank=True,
		help_text="Yangi taklif narxlari, ularning manbalari yoki joylari haqida ma’lumot"
	)
	offer_prices2 = models.TextField(
		blank=True,
		help_text="Yangi taklif narxlari, ularning manbalari yoki joylari haqida ma’lumot"
	)
	other_offers = models.TextField(blank=True, help_text="Qo'shimcha takliflar bo‘lsa, bu yerga yozing.")

	# Direktor o'rinbosari (boshlang‘ich rahbar) statusi
	DIRECTOR_STATUS_CHOICES = [
		('tasdiqlashda', 'Tasdiqlash jarayonida'),
		('tasdiqlandi', 'Tasdiqlandi'),
		('kutishda', 'Kutishda'),
		('rad_etildi', 'Rad etildi'),
	]
	director_status = models.CharField(max_length=20, choices=DIRECTOR_STATUS_CHOICES, default='tasdiqlashda')
	deputy_director_approved_at = models.DateTimeField(null=True, blank=True)

	# Ta’minot bo‘limi statusi
	SUPPLY_STATUS_CHOICES = [
		('jarayonda', 'Jarayonda'),
		('tugallandi', 'To‘liq bajarildi'),
		('bekor_qilindi', 'Bekor qilindi'),
	]
	supply_status = models.CharField(max_length=20, choices=SUPPLY_STATUS_CHOICES, default='jarayonda')
	supply_manager_completed_at = models.DateTimeField(null=True, blank=True)

	# Moliya bo‘limi statusi
	FINANCE_STATUS_CHOICES = [
		('tasdiqlashda', 'Tasdiqlash jarayonida'),
		('tasdiqlandi', 'Tasdiqlandi'),
		('kutishda', 'Kutishda'),
		('bekor_qilindi', 'Bekor qilindi'),
	]
	finance_status = models.CharField(max_length=20, choices=FINANCE_STATUS_CHOICES, default='tasdiqlashda')
	finance_approved_at = models.DateTimeField(null=True, blank=True)

	# Rahbar statusi
	LEADER_STATUS_CHOICES = [
		('tasdiqlashda', 'Tasdiqlash jarayonida'),
		('tasdiqlandi', 'Tasdiqlandi'),
		('kutishda', 'Kutishda'),
		('rad_etildi', 'Rad etildi'),
	]
	leader_status = models.CharField(max_length=20, choices=LEADER_STATUS_CHOICES, default='tasdiqlashda')
	leader_approved_at = models.DateTimeField(null=True, blank=True)

	# 	#Ombor bo`limi tastiqlashi uchun
	WAREHOUSE_STATUS_CHOICES = [
		('yetib_kelmagan', 'Yetib kelmagan'),
		('qabul_qilindi', 'Qabul qilindi'),
	]
	warehouse_status = models.CharField(max_length=20, choices=WAREHOUSE_STATUS_CHOICES, default='yetib_kelmagan', blank=True, null=True)
	transferred_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	warehouse_received_at = models.DateTimeField(null=True, blank=True)

	def approve_by_deputy_director(self):
		self.deputy_director_status = 'tasdiqlandi'
		self.deputy_director_approved_at = timezone.now()
		self.save()

	def complete_by_supply_manager(self):
		self.supply_manager_status = 'tugallandi'
		self.supply_manager_completed_at = timezone.now()
		self.save()

	def approve_by_finance(self):
		self.finance_status = 'tasdiqlandi'
		self.finance_approved_at = timezone.now()
		self.save()

	def approve_by_leader(self):
		self.leader_status = 'tasdiqlandi'
		self.leader_approved_at = timezone.now()
		self.save()

	def receive_by_warehouse(self):
		self.warehouse_status = 'qabul_qilindi'
		self.warehouse_received_at = timezone.now()
		self.save()

	def __str__(self):
		return f"{self.product_name} ({self.quantity} {self.unit_of_measure})"



















