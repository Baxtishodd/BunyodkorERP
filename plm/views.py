from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProductModel
from .forms import (ProductModelForm, EmployeeForm, OrderForm, WorkTypeForm, FabricArrivalForm, AccessoryForm,
                    CuttingForm)

from .models import (ProductionLine, Employee, HourlyWork, WorkType, Order, FabricArrival, Accessory, ModelAssigned,
                     Cutting)
from django.shortcuts import render, redirect
from datetime import time
from django.contrib import messages
from django.db.models import Sum
from collections import Counter

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

@login_required
def hourly_work_table(request, line_id, order_id):
    line = get_object_or_404(ProductionLine, id=line_id)
    employees = Employee.objects.filter(line=line)
    work_types = WorkType.objects.all()

    # Vaqt oralig‘i qo‘lda
    hours = [
        ("08:00", "09:00"),
        ("09:00", "10:00"),
        ("10:00", "11:00"),
        ("11:00", "12:00"),
        ("12:00", "13:00"),
        ("13:00", "14:00"),
        ("14:00", "15:00"),
        ("15:00", "16:00"),
        ("16:00", "17:00"),
        ("17:00", "17:45"),
    ]

    if request.method == "POST":
        for emp in employees:
            work_type_id = request.POST.get(f"emp{emp.id}_worktype")
            work_type = WorkType.objects.get(id=work_type_id) if work_type_id else None
            for idx, (start, end) in enumerate(hours):
                qty = request.POST.get(f"emp{emp.id}_slot{idx}", 0)
                if qty and int(qty) > 0:
                    # ✅ Yangi yozuvni bazaga saqlash
                    HourlyWork.objects.create(
                        employee=emp,
                        order_id=order_id,
                        work_type=work_type,
                        start_time=start,
                        end_time=end,
                        quantity=int(qty),
                    )
        return render(request, "planning/hourly_work_success.html", {"line": line, "order_id": order_id})

    return render(request, "planning/hourly_work_table.html", {
        "line": line,
        "order_id": order_id,
        "employees": employees,
        "work_types": work_types,
        "time_slots": hours,
    })

@login_required
def employee_list(request):
    employees = Employee.objects.select_related("line").all()
    return render(request, "employee/employee_list.html", {"employees": employees})

@login_required
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plm:employee_list')  # saqlangandan keyin list sahifaga yo'naltiradi
    else:
        form = EmployeeForm()
    return render(request, 'employee/employee_create.html', {'form': form})

@login_required
def worktype_list(request):
    worktypes = WorkType.objects.all().order_by('-id')  # oxirgi qo‘shilganlar birinchi chiqadi
    return render(request, "planning/worktype_list.html", {"worktypes": worktypes})

@login_required
def worktype_create(request):
    if request.method == 'POST':
        form = WorkTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plm:worktype_list')  # create tugagandan keyin list sahifasiga qaytadi
    else:
        form = WorkTypeForm()

    return render(request, 'planning/create_worktype.html', {'form': form})

@login_required
def productionline_list(request):
    lines = ProductionLine.objects.all()


    line_data = []
    for line in lines:
        employees_count = line.employee_set.count()  # hodimlar soni

        # Biriktirilgan model (oxirgisi yoki bir nechta bo‘lsa eng so‘nggisi)
        assigned = line.modelassigned_set.last()
        artikul = assigned.model_name.artikul if assigned else None
        client = assigned.model_name.client if assigned else None
        order_id = assigned.model_name.id if assigned else None
        quantity = assigned.model_name.quantity if assigned else 0

        # Normativ (oxirgisi)
        norm = line.norm_set.last()
        daily_norm = norm.daily_norm if norm else 0
        hourly_norm = norm.hourly_norm if norm else 0

        # Tikilgan mahsulot (masalan HourlyWork orqali)
        tikildi = line.hourlywork_set.aggregate(total=Sum("quantity"))["total"] or 0

        # Progress % (tikilgan / umumiy reja)
        progress = int((tikildi / quantity) * 100) if quantity else 0

        line_data.append({
            "pk": line.pk,
            "name": line.name,
            "client": client,
            "order_id": order_id,
            "employees_count": employees_count,
            "artikul": artikul,
            "quantity": quantity,
            "daily_norm": daily_norm,
            "hourly_norm": hourly_norm,
            "tikildi": tikildi,
            "progress": progress,
        })


    return render(request, "planning/productionline_list.html", {"lines": line_data})

@login_required
def productionline_detail(request, pk):
    line = get_object_or_404(ProductionLine, pk=pk)
    employees = line.employee_set.all()
    models_assigned = line.modelassigned_set.all()
    norms = line.norm_set.all().order_by('-created_at')

    return render(request, "planning/productionline_detail.html", {
        "line": line,
        "employees": employees,
        "models_assigned": models_assigned,
        "norms": norms,
    })

@login_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, "orders/order_list.html", {"orders": orders})

# Detail
@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "orders/order_detail.html", {"order": order})

# Create
@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            return redirect('plm:order_list')
    else:
        form = OrderForm()
    return render(request, "orders/order_form.html", {"form": form})

# Update
@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('plm:order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, "orders/order_form.html", {"form": form, "order": order})

# Delete
@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        messages.success(request, "Buyurtma muvaffaqiyatli o‘chirildi ✅")
        return redirect('plm:order_list')

    return render(request, "orders/order_confirm_delete.html", {"order": order})


# Mato tastiqlanish Ro‘yxat
@login_required
def fabric_list1(request):
    fabrics = FabricArrival.objects.select_related('order').order_by('-id')
    return render(request, 'planning/fabric/fabric_list.html', {'fabrics': fabrics})

@login_required
def fabric_list(request):
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    ).prefetch_related('fabric_arrival')

    return render(request, 'planning/fabric/fabric_list.html', {'orders': confirmed_orders})

@login_required
def fabric_add_to_order(request, order_id):
    # Faqat ModelAssigned orqali tasdiqlangan buyurtmaga qo‘shishga ruxsat beramiz
    is_confirmed = ModelAssigned.objects.filter(model_name_id=order_id).exists()
    order = get_object_or_404(Order, pk=order_id)

    if not is_confirmed:
        # agar bu buyurtma tasdiqlanmagan bo‘lsa, ro‘yxatga qaytarib yuboramiz
        return redirect('plm:fabric_list')

    if request.method == "POST":
        form = FabricArrivalForm(request.POST)
        if form.is_valid():
            fabric = form.save(commit=False)
            fabric.order = order
            fabric.author = request.user
            fabric.save()
            return redirect('plm:fabric_list')
    else:
        form = FabricArrival()
    return render(request, 'planning/fabric/fabric_form.html', {'form': form, 'order': order})


# Yangi qo‘shish
@login_required
def fabric_create(request):
    if request.method == 'POST':
        form = FabricArrivalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plm:fabric_list')
    else:
        form = FabricArrivalForm()
    return render(request, 'planning/fabric/fabric_form.html', {'form': form})

# Tasdiqlash
@login_required
def fabric_confirm(request, pk):
    fabric = get_object_or_404(FabricArrival, pk=pk)
    fabric.is_confirmed = True
    fabric.save()
    return redirect('plm:fabric_list')



# Aksessuarlar ro‘yxati — har bir buyurtmaga guruhlab chiqarish
# Faqat ModelAssigned orqali tasdiqlangan buyurtmalar

@login_required
def accessory_list(request):
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    ).prefetch_related('accessories')

    return render(request, 'planning/accessory/accessory_list.html', {'orders': confirmed_orders})

@login_required
def accessory_add_to_order(request, order_id):
    # Faqat ModelAssigned orqali tasdiqlangan buyurtmaga qo‘shishga ruxsat beramiz
    is_confirmed = ModelAssigned.objects.filter(model_name_id=order_id).exists()
    order = get_object_or_404(Order, pk=order_id)

    if not is_confirmed:
        # agar bu buyurtma tasdiqlanmagan bo‘lsa, ro‘yxatga qaytarib yuboramiz
        return redirect('plm:accessory_list')

    if request.method == "POST":
        form = AccessoryForm(request.POST)
        if form.is_valid():
            accessory = form.save(commit=False)
            accessory.order = order
            accessory.save()
            return redirect('plm:accessory_list')
    else:
        form = AccessoryForm()
    return render(request, 'planning/accessory/accessory_form.html', {'form': form, 'order': order})

# Aksessuar qo‘shish
@login_required
def accessory_create(request):
    if request.method == 'POST':
        form = AccessoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plm:accessory_list')
    else:
        form = AccessoryForm()
    return render(request, 'planning/accessory/accessory_form.html', {'form': form})


@login_required
def cutting_list(request):
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    ).prefetch_related('cuttings')

    orders_with_totals = []
    for order in confirmed_orders:
        jami_pastal = sum(c.pastal_soni for c in order.cuttings.all())
        orders_with_totals.append((order, jami_pastal))

    return render(
        request,
        'planning/cutting/cutting_list.html',
        {
            'orders_with_totals': orders_with_totals
        }
    )

@login_required
def cutting_add_to_order(request, order_id):
    # Faqat ModelAssigned orqali tasdiqlangan buyurtmaga qo‘shishga ruxsat beramiz
    is_confirmed = ModelAssigned.objects.filter(model_name_id=order_id).exists()
    order = get_object_or_404(Order, pk=order_id)

    if not is_confirmed:
        # agar bu buyurtma tasdiqlanmagan bo‘lsa, ro‘yxatga qaytarib yuboramiz
        return redirect('plm:cutting_list')

    if request.method == "POST":
        form = CuttingForm(request.POST)
        if form.is_valid():
            cutting = form.save(commit=False)
            cutting.order = order
            cutting.author = request.user
            cutting.save()
            return redirect('plm:cutting_list')
    else:
        form = CuttingForm()
    return render(request, 'planning/cutting/cutting_form.html', {'form': form, 'order': order})


@login_required
def cutting_update(request, pk):
    cutting = get_object_or_404(Cutting, pk=pk)
    if request.method == 'POST':
        form = CuttingForm(request.POST, instance=cutting)
        if form.is_valid():
            form.save()
            return redirect('plm:cutting_list')
    else:
        form = CuttingForm(instance=cutting)
    return render(request, 'planning/cutting/cutting_form.html', {'form': form})

@login_required
def cutting_delete(request, pk):
    cutting = get_object_or_404(Cutting, pk=pk)
    if request.method == 'POST':
        cutting.delete()
        return redirect('plm:cutting_list')
    return render(request, 'planning/cutting/cutting_confirm_delete.html', {'cutting': cutting})














































