from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

# my imports
from .forms import AddRecordForm, Add_Product_Form, ContactForm, AccountForm
from .models import Record, Product, Contact, Account

from django.views.generic import ListView

per_del_mess = "Sizda ma`lumotlarni o`chirish huquqi mavjud emas!"
per_add_mess = "Sizda ma`lumotlar qo`shish huquqi mavjud emas!"
per_upd_mess = "Sizda ma`lumotlarni o`zgartirish huquqi mavjud emas!"

now = timezone.now()

# Bosh sahifa
@login_required
def index_page(request):
	contact_count = Contact.objects.count()  # Count all contacts
	# Count all contacts in this month
	contacts_this_month = Contact.objects.filter(
		# created_at__year=now.year,
		created_at__month=now.month
	)

	print(f"Current UTC time: {now}")
	print(f"Year: {now.year}, Month: {now.month}")
	print(f"Contacts created this month: {contacts_this_month}")
	
	contacts = Contact.objects.all()
	for contact in contacts:
		print(contact.created_at)


	record_count = Record.objects.count()  # Count all employees
	account_count = Account.objects.count()  # Count all accounts

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
			return redirect('index')
		else:
			messages.warning(request, "Tizimga kirib bo`lmadi, keyinroq urinib ko`ring!")
			return redirect('index')


	context = {
		'contact_count': contact_count,
		'record_count': record_count,
		'account_count': account_count,

		'contact_this_month':contacts_this_month
	}


	return render(request, 'index.html', context)

# Xodimlar ro`yhati
@login_required
def records_view(request):
	# Check to see if logging in
	if request.user.has_perm('website.view_record'):
		records = Record.objects.all().order_by('-created_at') # Fetch all records from the database
		paginator = Paginator(records, 30)  # Show 30 records per page

		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)  # Get the current page records

		# search method
		query = request.GET.get('q')  # Get the search query from the URL


		if query:
			page_obj = Record.objects.filter(first_name__icontains=query) | \
					  Record.objects.filter(last_name__icontains=query) | \
					  Record.objects.filter(email__icontains=query) | \
					  Record.objects.filter(phone__icontains=query) | \
					  Record.objects.filter(country__icontains=query) | \
					  Record.objects.filter(state__icontains=query) | \
					  Record.objects.filter(city__icontains=query)
			return render(request, 'home.html', {'records':page_obj})

		else:
			return render(request, 'home.html', {'records':page_obj})
	else:
		messages.success(request, "Sizda bu ma'lumotlarni ko'rish huquqi yo'q!")
		return redirect('index')

@login_required
def dashboard_view(request, pk=1):
	if request.user.is_authenticated:
		user = Record.objects.get(id=pk)
		return render(request, 'dashboard.html', {'dashboard_view': user})


###			start record  		###
@login_required
def customer_record(request, pk):
	if request.user.is_authenticated:
		if request.user.has_perm('website.view_record'):
			# Look Up Records
			customer_record = Record.objects.get(id=pk)
			return render(request, 'record.html', {'customer_record':customer_record})
		else:
			messages.success(request, "Sizda bu ma'lumotni ko'rish huquqi yo'q!")
			return redirect('index')
	else:
		messages.success(request, "Siz ro`yhatdan o`tgan bo`lishingiz lozim!")
		return redirect('records')

@login_required
def delete_record(request, pk):
	if request.user.is_authenticated:
		if request.user.has_perm('website.delete_record'):
			delete_it = Record.objects.get(id=pk)
			delete_it.delete()
			messages.warning(request, "Ma`lumotlar o`chirildi!")
			return redirect('records')
		else:
			messages.success(request, per_del_mess)
			return redirect('records')
	else:
		messages.success(request, "Siz ro`yhatdan o`tgan bo`lishingiz lozim!")
		return redirect('index')

@login_required
@permission_required('website.add_record', raise_exception=False)
def add_record(request):
	form = AddRecordForm(request.POST or None, request.FILES )
	if request.user.is_authenticated:
		if request.user.has_perm('website.add_record'):
			if request.method == "POST":
				if form.is_valid():
					record = form.save(commit=False)
					record.created_by = request.user
					record.save()
					messages.success(request, "Ma`lumotlar qo`shildi!")
					return redirect('records')
				else:
					messages.success(request, "Ma`lumotlar qo`shilmadi! Formada qandaydir xatolik mavjud!")
			return render(request, 'add_record.html', {'form':form})
		else:
			messages.success(request, per_add_mess)
			return redirect('index')
	else:
		messages.success(request, "Siz ro`yhatdan o`tgan bo`lishingiz lozim!")
		return redirect('index')


@login_required
def update_record(request, pk):
	# Check if the user is authenticated
	if request.user.is_authenticated:
		# Check if the user has the permission to update records
		if request.user.has_perm('website.change_record'):
			# Get the record or return 404 if not found
			current_record = get_object_or_404(Record, id=pk)

			# Handle POST request with file uploads (images, etc.)
			form = AddRecordForm(request.POST or None, request.FILES or None, instance=current_record)

			if form.is_valid():
				form.save()
				messages.success(request, "Ma'lumotlar o'zgartirildi!")
				return redirect('records')  # Redirect to the records list or another relevant view
			# else:
			# 	messages.error(request, "Formada xatolik bor, iltimos qaytadan tekshiring!")

			return render(request, 'update_record.html', {'form': form, 'record': current_record})

		else:
			# If user doesn't have permission
			messages.error(request, "Sizda bu ma'lumotni yangilash huquqi yo'q!")
			return redirect('index')

	else:
		# If user is not authenticated
		messages.error(request, "Siz ro'yhatdan o'tgan bo'lishingiz lozim!")
		return redirect('index')

### 		End record		###

###			start Product	###
def products(request):
	products = Product.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "Tizimga kirgansiz!")
			return redirect('products')
		else:
			messages.success(request, "Siz ro`yhatdan o`tgan bo`lishingiz lozim!")
			return redirect('products')
	else:
		return render(request, 'product_list.html', {'products':products})


def product_record(request, pk):
	if request.user.is_authenticated:
		product_record = Product.objects.get(id=pk)
		return render(request, 'product.html', {'product_add': product_record})
	else:
		messages.success(request, "Siz ro`yhatdan o`tgan bo`lishingiz lozim!")
		return redirect('index')


def delete_product(request, pk):
	if request.user.is_authenticated:
		delete_it = Product.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Model o`chirildi")
		return redirect('product')
	else:
		messages.success(request, "Siz ro`yhatdan o`tgan bo`lishingiz lozim!")
		return redirect('product')


def add_product(request):
	form = Add_Product_Form(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_product = form.save()
				messages.success(request, "Model qo`shildi")
				return redirect('add_product')
		return render(request, 'add_product.html', {'form':form})
	else:
		messages.success(request, "Siz ro`yhatdan o`tgan bo`lishingiz lozim!")
		return redirect('add_product')


def update_product(request):
	form = None


# Contacts model
# List Contacts

@login_required
def contact_list(request):
	if request.user.has_perm('website.view_contact'):
		# Start with all contacts
		contacts = Contact.objects.all().order_by('-created_at')
		form = ContactForm()

		# Determine which view to render
		view_type = request.GET.get('view', 'list')  # Default to 'list' view

		# Search functionality
		query = request.GET.get('q')  # Get the search query from the URL
		if query:
			contacts = contacts.filter(
				first_name__icontains=query
			) | contacts.filter(
				last_name__icontains=query
			) | contacts.filter(
				created_by__username__icontains=query
			)

		# Filtering functionality
		lead_status = request.GET.get('lead_status')
		industry = request.GET.get('industry')
		account_manager = request.GET.get('account_manager')

		# Apply filters if values are provided
		if lead_status:
			contacts = contacts.filter(lead_status=lead_status)

		if account_manager:
			contacts = contacts.filter(account_manager__id=account_manager)

		# Sorting functionality
		sort_by = request.GET.get('sort', 'created_at')  # Default to 'created_at' field
		direction = request.GET.get('direction', 'desc')  # Default to descending

		# Validate sort_by field to avoid sorting by invalid fields
		valid_sort_fields = ['first_name', 'lead_status', 'email', 'company_name', 'phone_mobile', 'created_by']
		if sort_by not in valid_sort_fields:
			sort_by = 'created_at'

		# Add ordering direction
		if direction == 'asc':
			contacts = contacts.order_by(sort_by)
		else:
			contacts = contacts.order_by(f'-{sort_by}')

		# Pagination logic based on view type
		if view_type == 'cards':
			items_per_page = 15  # Card view: 12 items per page
		else:
			items_per_page = 15  # List view: 30 items per page

		# Pagination
		paginator = Paginator(contacts, items_per_page)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)  # Get the current page contacts


		# # Sorting functionality
		# sort_by = request.GET.get('sort', 'created_at')  # Default to 'created_at' field
		# direction = request.GET.get('direction', 'desc')  # Default to descending
		#
		# # Add ordering direction
		# if direction == 'asc':
		# 	contacts = contacts.order_by(sort_by)
		# else:
		# 	contacts = contacts.order_by(f'-{sort_by}')


		# Get distinct values for filters
		industries = Contact.objects.values('industry').distinct()
		account_managers = Contact.objects.values('account_manager').distinct()


		if view_type == 'cards':
			template_name = 'contacts/contact_list_card.html'
		else:
			template_name = 'contacts/contact_list.html'

		return render(request, template_name, {
			'contact_form':form,
			'contacts': page_obj,
			'query': query,  # Pass the query back to the template to retain it in the search box
			'lead_status': lead_status,  # Pass lead status to retain in the filter dropdown
			'industry': industry,  # Pass industry to retain in the filter dropdown
			'account_manager': account_manager,  # Pass account manager to retain in the filter dropdown
			'industries': industries,  # Pass industries for filter dropdown options
			'account_managers': account_managers,  # Pass account managers for filter dropdown options
			'sort_by': sort_by,  # Pass the current sort field to the template
			'direction': direction,  # Pass the current direction to the template
			'view_type': view_type,  # Pass current view type to the template for links/buttons

		})
	else:
		messages.error(request, "Sizda bu ma'lumotni ko'rish huquqi yo'q!")
		return redirect('index')

# Add New Contact
@login_required
def contact_create(request):
	if not request.user.has_perm('website.add_contact'):
		messages.error(request, "Sizda yangi kontakt qo'shish huquqi yo'q!")
		return redirect('index')

	if request.method == 'POST':
		form = ContactForm(request.POST, request.FILES)
		if form.is_valid():
			contact = form.save(commit=False)
			contact.created_by = request.user
			contact.save()
			messages.success(request, "Yangi kontakt muvaffaqiyatli qo'shildi!")
			return redirect('contact_list')
	else:
		form = ContactForm()

	return render(request, 'contacts/contact_form.html', {'form': form})

# Edit Contact
@login_required
@permission_required('website.change_contact', raise_exception=False)
def contact_edit(request, pk):
	contact = get_object_or_404(Contact, id=pk)
	if contact.created_by == request.user:

		if request.method == 'POST':
			form = ContactForm(request.POST, request.FILES, instance=contact)
			if form.is_valid():
				form.save()
				return redirect('contact_list')
		else:
			form = ContactForm(instance=contact)
		return render(request, 'contacts/contact_form.html', {'form': form})
	else:
		messages.error(request, "Sizda kontaktni o'zgartitish huquqi yo'q!")
		return redirect('contact_list')


@login_required
@permission_required('website.delete_contact', raise_exception=False)
def contact_delete(request, pk):
	# Use get_object_or_404 for better error handling
	delete_it = get_object_or_404(Contact, id=pk)

	# Check if the contact was created by the logged-in user
	if delete_it.created_by == request.user:
		delete_it.delete()
		messages.warning(request, "Ma`lumotlar o`chirildi!")  # Message for successful deletion
	else:
		# If the user is not the creator, show an error message
		messages.error(request, "Siz faqat o'zingiz yaratgan ma'lumotlarni o'chirishingiz mumkin!")

	return redirect('contact_list')


# Account view start
@login_required
def account_create(request):
	if not request.user.has_perm('website.add_account'):
		messages.error(request, "Sizda yangi akkaunt qo'shish huquqi yo'q!")
		return redirect('index')

	if request.method == 'POST':
		form = AccountForm(request.POST, request.FILES)
		if form.is_valid():
			account = form.save(commit=False)
			account.account_manager = request.user
			account.save()
			messages.success(request, "Yangi account muvaffaqiyatli qo'shildi!")
			return redirect('accounts')
	else:
		form = AccountForm()

	return render(request, 'accounts/account_form.html', {'form': form})


class AccountListView(LoginRequiredMixin, ListView):
	model = Account
	template_name = 'accounts/account_list.html'  # Customize your template path if necessary
	context_object_name = 'accounts'  # Name for the accounts in the template
	paginate_by = 10  # Optional: Add pagination, 10 accounts per page
	login_url = '/login/'  # The URL to redirect to for login if needed

	# def get_queryset(self):
	# 	# You can customize the queryset if needed, e.g., filter by some condition
	# 	return Account.objects.all().order_by('account_name')

	def get_queryset(self):
		# Get the base queryset
		queryset = Account.objects.all().order_by('account_name')

		# Get the search query
		query = self.request.GET.get('q')
		if query:
			# Use Q objects to perform a case-insensitive search across multiple fields
			queryset = queryset.filter(
				Q(account_name__icontains=query) |
				Q(account_manager__username__icontains=query)  # Adjust based on your fields
			)

		return queryset







