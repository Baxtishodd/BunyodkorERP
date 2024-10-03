from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required


# my imports
from .forms import AddRecordForm, Add_Product_Form, ContactForm
from .models import Record, Product, Contact

per_del_mess = "Sizda ma`lumotlarni o`chirish huquqi mavjud emas!"
per_add_mess = "Sizda ma`lumotlar qo`shish huquqi mavjud emas!"
per_upd_mess = "Sizda ma`lumotlarni o`zgartirish huquqi mavjud emas!"


# Bosh sahifa
def index_page(request):
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

	return render(request, 'index.html')

# Xodimlar ro`yhati
def records_view(request):
	records = Record.objects.all().order_by('-created_at') # Fetch all records from the database
	paginator = Paginator(records, 30)  # Show 30 records per page

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)  # Get the current page records

	# search method
	query = request.GET.get('q')  # Get the search query from the URL

	# Check to see if logging in
	if request.user.is_authenticated:
	# if request.method == 'POST':
	# 	username = request.POST['username']
	# 	password = request.POST['password']
	# 	# Authenticate
	# 	user = authenticate(request, username=username, password=password)
	# 	if user is not None:
	# 		login(request, user)
	# 		messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
	# 		return redirect('records')
	# 	else:
	# 		messages.warning(request, "Tizimga kirib bo`lmadi, keyinroq urinib ko`ring!")
	# 		return redirect('records')
	# search method
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
		messages.success(request, "Tizimga login qilib kirishingiz lozim!")
		return redirect('index')


def dashboard_view(request, pk=1):
	if request.user.is_authenticated:
		user = Record.objects.get(id=pk)
		return render(request, 'dashboard.html', {'dashboard_view': user})


###			start record  		###
def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "Siz ro`yhatdan o`tgan bo`lishingiz lozim!")
		return redirect('records')


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


def update_record(request, pk):
	# Check if the user is authenticated
	if request.user.is_authenticated:
		# Check if the user has the permission to update records
		if request.user.has_perm('website.update_record'):
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


# Contacts
# List Contacts
def contact_list(request):
	contacts = Contact.objects.all()
	return render(request, 'contacts/contact_list.html', {'contacts': contacts})

# Add New Contact
def contact_create(request):
	if request.method == 'POST':
		form = ContactForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('contact_list')
	else:
		form = ContactForm()
	return render(request, 'contacts/contact_form.html', {'form': form})

# Edit Contact
def contact_edit(request, pk):
	contact = get_object_or_404(Contact, pk=pk)
	if request.method == 'POST':
		form = ContactForm(request.POST, request.FILES, instance=contact)
		if form.is_valid():
			form.save()
			return redirect('contact_list')
	else:
		form = ContactForm(instance=contact)
	return render(request, 'contacts/contact_form.html', {'form': form})

@login_required
@permission_required('website.delete_contact', raise_exception=True)
def contact_delete(request, pk):
	# Use get_object_or_404 for better error handling
	delete_it = get_object_or_404(Contact, id=pk)
	delete_it.delete()
	messages.warning(request, "Ma`lumotlar o`chirildi!")  # Message for successful deletion
	return redirect('contact_list')











