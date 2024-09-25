from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import AddRecordForm, Add_Product_Form
from .models import Record, Product


per_del_mess = "Sizda ma`lumotlarni o`chirish huquqi mavjud emas!"
per_add_mess = "Sizda ma`lumotlar qo`shish huquqi mavjud emas!"
per_upd_mess = "Sizda ma`lumotlarni o`zgartirish huquqi mavjud emas!"

def home(request):
	records = Record.objects.all() # Fetch all records from the database
	paginator = Paginator(records, 30)  # Show 30 records per page

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)  # Get the current page records

	# search method
	query = request.GET.get('q')  # Get the search query from the URL

	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
			return redirect('home')
		else:
			messages.warning(request, "Tizimga kirib bo`lmadi, keyinroq urinib ko`ring!")
			return redirect('home')
	# search method
	elif query:
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


def logout_user(request):
	logout(request)
	messages.success(request, "Tizimdan chiqdingiz!")
	return redirect('home')


# def register_user(request):
# 	if request.method == 'POST':
# 		form = SignUpForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			# Authenticate and login
# 			username = form.cleaned_data['username']
# 			password = form.cleaned_data['password1']
# 			user = authenticate(username=username, password=password)
# 			login(request, user)
# 			messages.success(request, "Siz muvaffaqiyatli ro`yhatdan o`tdingiz!")
# 			return redirect('home')
# 	else:
# 		form = SignUpForm()
# 		return render(request, 'register.html', {'form':form})
#
# 	return render(request, 'register.html', {'form':form})


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
		return redirect('home')



def delete_record(request, pk):
	if request.user.is_authenticated:
		if request.user.has_perm('website.delete_record'):
			delete_it = Record.objects.get(id=pk)
			delete_it.delete()
			messages.warning(request, "Ma`lumotlar o`chirildi!")
			return redirect('home')
		else:
			messages.success(request, per_del_mess)
			return redirect('home')
	else:
		messages.success(request, "Siz ro`yhatdan o`tgan bo`lishingiz lozim!")
		return redirect('home')


def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.user.has_perm('website.add_record'):
			if request.method == "POST":
				if form.is_valid():
					add_record = form.save()
					messages.success(request, "Ma`lumotlar qo`shildi!")
					return redirect('home')
				else:
					messages.success(request, "Ma`lumotlar qo`shilmadi! Formada qandaydir xatolik mavjud!")
			return render(request, 'add_record.html', {'form':form})
		else:
			messages.success(request, per_add_mess)
			return redirect('home')
	else:
		messages.success(request, "Siz ro`yhatdan o`tgan bo`lishingiz lozim!")
		return redirect('home')


def update_record(request, pk):
	if request.user.is_authenticated:
		if request.user.has_perm('website.update_record'):
			current_record = Record.objects.get(id=pk)
			form = AddRecordForm(request.POST or None, instance=current_record)
			if form.is_valid():
				form.save()
				messages.success(request, "Ma`lumotlar o`zgartirildi!")
				return redirect('home')
			return render(request, 'update_record.html', {'form':form})
		else:
			messages.success(request, per_upd_mess)
			return redirect('home')
	else:
		messages.success(request, "Siz ro`yhatdan o`tgan bo`lishingiz lozim!")
		return redirect('home')

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
		return redirect('home')


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
















