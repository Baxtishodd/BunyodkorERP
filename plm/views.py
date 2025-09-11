from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProductModel
from .forms import ProductModelForm  # form yaratamiz

# Model kartalar ro‘yxati
@login_required
def productmodel_list(request):
    products = ProductModel.objects.all()
    return render(request, "plm/productmodel_list.html", {"products": products})


# Bitta model kartani ko‘rish
@login_required
def productmodel_detail(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)
    return render(request, "plm/productmodel_detail.html", {"product": product})


# Yangi model qo‘shish
@login_required
def productmodel_create(request):
    if request.method == "POST":
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect("plm:productmodel_list")
    else:
        form = ProductModelForm()
    return render(request, "plm/productmodel_form.html", {"form": form})


# Modelni yangilash
@login_required
def productmodel_update(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)
    if request.method == "POST":
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("plm:productmodel_list")
    else:
        form = ProductModelForm(instance=product)
    return render(request, "plm/productmodel_form.html", {"form": form})


# Modelni o‘chirish
@login_required
def productmodel_delete(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("plm:productmodel_list")
    return render(request, "plm/productmodel_confirm_delete.html", {"product": product})
