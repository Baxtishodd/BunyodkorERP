from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProductModel, Printing
from .forms import (ProductModelForm, EmployeeForm, OrderForm, WorkTypeForm, FabricArrivalForm, AccessoryForm,
                    CuttingForm, PrintForm, OrderSizeForm, StitchingForm, IroningForm, InspectionForm, PackingForm,
                    ShipmentForm)

from .models import (ProductionLine, Employee, HourlyWork, WorkType, Order, FabricArrival, Accessory, ModelAssigned,
                     Cutting, OrderSize, Stitching, Ironing, Inspection, Packing, Shipment)
from django.shortcuts import render, redirect
from datetime import time
from django.contrib import messages
from django.db.models import Sum
from collections import Counter, defaultdict

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
        if assigned:
            order = assigned.model_name  # Order object
            artikul = order.artikul
            client = order.client
            order_id = order.id
            quantity = order.sum_order_size() or 0
            print(f"Line: {line.name}, Order: {order}, Quantity: {quantity}")  # 🔍 Debug
        else:
            artikul = None
            client = None
            order_id = None
            quantity = 0

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


    return render(request, "planning/line/productionline_list.html", {"lines": line_data})

@login_required
def productionline_detail(request, pk):
    line = get_object_or_404(ProductionLine, pk=pk)
    employees = line.employee_set.all()
    models_assigned = line.modelassigned_set.all()
    norms = line.norm_set.all().order_by('-created_at')

    return render(request, "planning/line/productionline_detail.html", {
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
    sum_order_size = sum(c.quantity or 0 for c in order.ordersize.all())

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
            "sum_order_size": sum_order_size
        }
    )
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

@login_required
def ordersize_list(request, pk):
    order = get_object_or_404(Order, pk=pk)
    sum_order_size = sum(c.quantity for c in order.ordersize.all())

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order,
            'sum_order_size': sum_order_size
        }
    )


@login_required
def ordersize_add_to_order(request, pk):

    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        form = OrderSizeForm(request.POST)
        if form.is_valid():
            ordersize = form.save(commit=False)
            ordersize.order = order
            ordersize.author = request.user
            ordersize.save()
            return redirect('plm:order_detail', pk=order.pk)
    else:
        form = OrderSizeForm()
    return render(request, 'orders/ordersize/ordersize_form.html', {'form': form, 'order': order})


@login_required
def ordersize_update(request, pk):
    ordersize = get_object_or_404(OrderSize, pk=pk)
    order = ordersize.order

    if request.method == "POST":
        form = OrderSizeForm(request.POST, instance=ordersize)
        if form.is_valid():
            form.save()
            return redirect("plm:order_detail", pk=order.pk)
    else:
        form = OrderSizeForm(instance=ordersize)
    return render(request, "orders/ordersize/ordersize_form.html", {"form": form, "title": "O‘lchamni tahrirlash"})


@login_required
def ordersize_delete(request, pk):
    ordersize = get_object_or_404(OrderSize, pk=pk)
    order = ordersize.order

    if request.method == "POST":
        ordersize.delete()
        messages.success(request, "Buyurtma o'lchami muvaffaqiyatli o‘chirildi ✅")
        return redirect("plm:order_detail", pk=order.pk)
    return render(request, "orders/ordersize/ordersize_confirm_delete.html", {"ordersize": ordersize})

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
        return redirect("plm:plan_order_detail", order_id=is_confirmed.order.pk)

    if request.method == "POST":
        form = FabricArrivalForm(request.POST)
        if form.is_valid():
            fabric = form.save(commit=False)
            fabric.order = order
            fabric.author = request.user
            fabric.save()
            return redirect("plm:plan_order_detail", order_id=fabric.order.pk)
    else:
        form = FabricArrivalForm()
    return render(request, 'planning/fabric/fabric_form.html', {'form': form, 'order': order})


# Tasdiqlash
@login_required
def fabric_confirm(request, pk):
    fabric = get_object_or_404(FabricArrival, pk=pk)
    fabric.is_confirmed = True
    fabric.save()
    return redirect("plm:plan_order_detail", order_id=fabric.order.pk)


@login_required
def fabric_update(request, pk):
    fabric = get_object_or_404(FabricArrival, pk=pk)
    if request.method == 'POST':
        form = FabricArrivalForm(request.POST, instance=fabric)
        if form.is_valid():
            form.save()
            messages.success(request, "Mato ma'lumoti yangilandi ✅")
            return redirect("plm:plan_order_detail", order_id=fabric.order.pk)
    else:
        form = FabricArrivalForm(instance=fabric)
    return render(request, 'planning/fabric/fabric_form.html', {'form': form, 'fabric': fabric})


@login_required
def fabric_delete(request, pk):
    fabric = get_object_or_404(FabricArrival, pk=pk)
    if request.method == 'POST':
        fabric.delete()
        messages.success(request, "Mato ma'lumoti o‘chirildi ❌")
        return redirect("plm:plan_order_detail", order_id=fabric.order.pk)

    return render(request, 'planning/fabric/fabric_confirm_delete.html', {'fabric': fabric})


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
            return redirect("plm:plan_order_detail", order_id=accessory.order.pk)
    else:
        form = AccessoryForm()
    return render(request, 'planning/accessory/accessory_form.html', {'form': form, 'order': order})


@login_required
def accessory_update(request, pk):
    accessory = get_object_or_404(Accessory, pk=pk)
    order = accessory.order

    if request.method == 'POST':
        form = AccessoryForm(request.POST, instance=accessory)
        if form.is_valid():
            form.save()
            return redirect("plm:plan_order_detail", order_id=accessory.order.pk)
    else:
        form = AccessoryForm(instance=accessory)
    return render(request, 'planning/accessory/accessory_form.html', {'form': form, 'order':order})

@login_required
def accessory_delete(request, pk):
    accessory = get_object_or_404(Accessory, pk=pk)
    if request.method == 'POST':
        accessory.delete()
        return redirect("plm:plan_order_detail", order_id=accessory.order.pk)
    return render(request, 'planning/accessory/accessory_confirm_delete.html', {'accessory': accessory})



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

    if request.method == "POST":
        form = CuttingForm(request.POST)
        if form.is_valid():
            cutting = form.save(commit=False)
            cutting.order = order
            cutting.author = request.user
            cutting.save()
            return redirect("plm:plan_order_detail", order_id=cutting.order.pk)
    else:
        form = CuttingForm()
    return render(request, 'planning/cutting/cutting_form.html', {'form': form, 'order': order})


@login_required
def cutting_update(request, pk):
    cutting = get_object_or_404(Cutting, pk=pk)
    order = cutting.order

    if request.method == 'POST':
        form = CuttingForm(request.POST, instance=cutting)
        if form.is_valid():
            form.save()
            return redirect("plm:plan_order_detail", order_id=cutting.order.pk)
    else:
        form = CuttingForm(instance=cutting)
    return render(request, 'planning/cutting/cutting_form.html', {'form': form, 'order':order})

@login_required
def cutting_delete(request, pk):
    cutting = get_object_or_404(Cutting, pk=pk)
    if request.method == 'POST':
        cutting.delete()
        return redirect("plm:plan_order_detail", order_id=cutting.order.pk)
    return render(request, 'planning/cutting/cutting_confirm_delete.html', {'cutting': cutting})


# Printing view
@login_required
def print_list(request):
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    ).prefetch_related('prints')

    orders_with_totals = []
    for order in confirmed_orders:
        jami_pechat = sum(c.quantity for c in order.prints.all())
        orders_with_totals.append((order, jami_pechat))

    return render(
        request,
        'planning/print/print_list.html',
        {
            'orders_with_totals': orders_with_totals
        }
    )
    # return render(request, 'planning/print/print_list.html', {'orders': confirmed_orders})

@login_required
def print_add_to_order(request, order_id):
    # Faqat ModelAssigned orqali tasdiqlangan buyurtmaga qo‘shishga ruxsat beramiz
    is_confirmed = ModelAssigned.objects.filter(model_name_id=order_id).exists()
    order = get_object_or_404(Order, pk=order_id)

    if not is_confirmed:
        # agar bu buyurtma tasdiqlanmagan bo‘lsa, ro‘yxatga qaytarib yuboramiz
        return redirect('plm:print_list')

    if request.method == "POST":
        form = PrintForm(request.POST)
        if form.is_valid():
            print = form.save(commit=False)
            print.order = order
            print.created_by = request.user
            print.save()
            return redirect("plm:plan_order_detail", order_id=print.order.pk)
    else:
        form = PrintForm()
    return render(request, 'planning/print/print_form.html', {'form': form, 'order': order})



@login_required
def print_update(request, pk):
    print_obj = get_object_or_404(Printing, pk=pk)
    order = print_obj.order

    if request.method == 'POST':
        form = PrintForm(request.POST, instance=print_obj)
        if form.is_valid():
            form.save()
            return redirect("plm:plan_order_detail", order_id=print_obj.order.pk)
    else:
        form = PrintForm(instance=print_obj)
    return render(request, 'planning/print/print_form.html', {'form': form, 'order': order})


@login_required
def print_delete(request, pk):
    print = get_object_or_404(Printing, pk=pk)
    if request.method == 'POST':
        print.delete()
        return redirect("plm:plan_order_detail", order_id=print.order.pk)
    return render(request, 'planning/print/print_confirm_delete.html', {'print': print})


@login_required
def stitching_list(request):
    confirmed_orders = (
        Order.objects.filter(
            id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
        )
        .prefetch_related("ordersize__stitchings")
        .order_by("created_at")
    )

    # Har bir order uchun jami tikilgan o‘lchamlar lug‘ati
    order_size_totals = {}
    order_total_quantity = {}

    for order in confirmed_orders:
        size_totals = defaultdict(int)
        total_quantity = 0

        for ordersize in order.ordersize.all():
            stitched_sum = ordersize.stitchings.aggregate(total=Sum("quantity"))["total"] or 0
            size_totals[ordersize.size] += stitched_sum
            total_quantity += stitched_sum

        order_size_totals[order.id] = dict(size_totals)
        order_total_quantity[order.id] = total_quantity

    return render(
        request,
        "planning/stitching/stitching_list.html",
        {
            "orders": confirmed_orders,
            "order_size_totals": order_size_totals,
            "order_total_quantity": order_total_quantity,
        },
    )

@login_required
def stitching_add(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    # shu orderga bog‘langan patok(lar)
    assigned_lines = ModelAssigned.objects.filter(model_name=order).select_related("line")

    if request.method == "POST":
        form = StitchingForm(request.POST, order=order)
        if form.is_valid():
            stitching = form.save(commit=False)
            # Patok yoki sexni avtomatik qo‘shish kerak bo‘lsa shu yerga qo‘shiladi
            stitching.save()
            return redirect("plm:plan_order_detail", order_id=stitching.order.pk)
    else:
        form = StitchingForm(order=order)

    return render(
        request,
        "planning/stitching/stitching_form.html",
        {"form": form, "order": order,  "assigned_lines": assigned_lines,},
    )

@login_required
def stitching_update(request, pk):
    stitching = get_object_or_404(Stitching, pk=pk)
    order = stitching.ordersize.order

    if request.method == "POST":
        form = StitchingForm(request.POST, instance=stitching, order=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Tikim ma'lumoti yangilandi ✅")
            return redirect("plm:plan_order_detail", order_id=stitching.order.pk)
    else:
        form = StitchingForm(instance=stitching, order=order)

    return render(request, "planning/stitching/stitching_form.html", {
        "form": form,
        "order": order,
    })

@login_required
def stitching_delete(request, pk):
    stitching = get_object_or_404(Stitching, pk=pk)
    order = stitching.ordersize.order
    if request.method == "POST":
        stitching.delete()
        messages.success(request, "Tikim ma'lumoti o‘chirildi ❌")
        return redirect("plm:plan_order_detail", order_id=stitching.order.pk)

    return render(request, "planning/stitching/stitching_confirm_delete.html", {"stitching": stitching})


# Ironing view Dazmol modeli
@login_required
def ironing_list(request):
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    ).prefetch_related('ironing')

    orders_with_totals = []
    for order in confirmed_orders:
        jami_dazmol = sum(c.quantity for c in order.ironing.all())
        orders_with_totals.append((order, jami_dazmol))

    return render(
        request,
        'planning/ironing/ironing_list.html',
        {
            'orders_with_totals': orders_with_totals
        }
    )

@login_required
def ironing_add_to_order(request, order_id):
    # Faqat ModelAssigned orqali tasdiqlangan buyurtmaga qo‘shishga ruxsat beramiz
    is_confirmed = ModelAssigned.objects.filter(model_name_id=order_id).exists()
    order = get_object_or_404(Order, pk=order_id)

    if not is_confirmed:
        # agar bu buyurtma tasdiqlanmagan bo‘lsa, ro‘yxatga qaytarib yuboramiz
        return redirect("plm:plan_order_detail", order_id=is_confirmed.order.pk)

    if request.method == "POST":
        form = IroningForm(request.POST)
        if form.is_valid():
            ironing = form.save(commit=False)
            ironing.order = order
            ironing.created_by = request.user
            ironing.save()
            return redirect("plm:plan_order_detail", order_id=ironing.order.pk)
    else:
        form = IroningForm()
    return render(request, 'planning/ironing/ironing_form.html', {'form': form, 'order': order})

@login_required
def ironing_update(request, pk):
    ironing_obj = get_object_or_404(Ironing, pk=pk)
    order = ironing_obj.order

    if request.method == 'POST':
        form = IroningForm(request.POST, instance=ironing_obj)
        if form.is_valid():
            form.save()
            return redirect("plm:plan_order_detail", order_id=ironing_obj.order.pk)
    else:
        form = IroningForm(instance=ironing_obj)
    return render(request, 'planning/ironing/ironing_form.html', {'form': form, 'order': order})

@login_required
def ironing_delete(request, pk):
    ironing = get_object_or_404(Ironing, pk=pk)
    if request.method == 'POST':
        ironing.delete()
        return redirect("plm:plan_order_detail", order_id=ironing.order.pk)
    return render(request, 'planning/ironing/ironing_confirm_delete.html', {'ironing': ironing})


# Inspection VIEW
@login_required
def inspection_list(request):
    """Barcha inspectionlar ro‘yxati va umumiy statistikasi"""
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    ).prefetch_related('inspections')

    orders_with_totals = []
    total_checked_sum = 0
    passed_sum = 0
    failed_sum = 0

    for order in confirmed_orders:
        order_total_checked = sum(i.total_checked for i in order.inspections.all())
        order_passed = sum(i.passed_quantity for i in order.inspections.all())
        order_failed = sum(i.failed_quantity for i in order.inspections.all())

        total_checked_sum += order_total_checked
        passed_sum += order_passed
        failed_sum += order_failed

        orders_with_totals.append({
            "order": order,
            "total_checked": order_total_checked,
            "passed": order_passed,
            "failed": order_failed,
        })

    return render(
        request,
        "planning/inspection/inspection_list.html",
        {
            "orders_with_totals": orders_with_totals,
            "total_checked_sum": total_checked_sum,
            "passed_sum": passed_sum,
            "failed_sum": failed_sum,
        },
    )

@login_required
def inspection_add_to_order(request, order_id):
    """Orderga yangi inspection qo‘shish"""
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        form = InspectionForm(request.POST)
        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.order = order
            inspection.created_by = request.user
            inspection.save()
            messages.success(request, "Sifat nazorati muvaffaqiyatli qo‘shildi ✅")
            return redirect("plm:plan_order_detail", order_id=inspection.order.pk)
    else:
        form = InspectionForm()

    return render(request, "planning/inspection/inspection_form.html", {"form": form, "order": order})

@login_required
def inspection_update(request, pk):
    """Inspection ma'lumotlarini tahrirlash"""
    inspection = get_object_or_404(Inspection, pk=pk)
    order = inspection.order  # Bog‘langan buyurtma

    if request.method == "POST":
        form = InspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            messages.success(request, "Sifat nazorati ma'lumotlari yangilandi.")
            return redirect("plm:plan_order_detail", order_id=inspection.order.pk)
    else:
        form = InspectionForm(instance=inspection)

    return render(
        request,
        "planning/inspection/inspection_form.html",
        {
            "form": form,
            "order": order,
        },
    )

@login_required
def inspection_delete(request, pk):
    """Inspectionni o‘chirish"""
    inspection = get_object_or_404(Inspection, pk=pk)
    order_id = inspection.order.id

    if request.method == "POST":
        inspection.delete()
        messages.success(request, "Sifat nazorati yozuvi o‘chirildi 🗑️")
        return redirect("plm:plan_order_detail", order_id=inspection.order.pk)

    return render(request, "planning/inspection/inspection_confirm_delete.html", {"inspection": inspection})

# Packing VIEW
@login_required
def packing_list(request):
    """Barcha packinglar ro‘yxati va umumiy statistikasi"""
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    ).prefetch_related("packings")

    orders_with_totals = []
    total_products_sum = 0
    total_boxes_sum = 0

    for order in confirmed_orders:
        order_total_products = sum(p.product_quantity for p in order.packings.all())
        order_total_boxes = sum(p.box_quantity for p in order.packings.all())

        total_products_sum += order_total_products
        total_boxes_sum += order_total_boxes

        orders_with_totals.append({
            "order": order,
            "product_quantity": order_total_products,
            "box_quantity": order_total_boxes,
        })

    return render(
        request,
        "planning/packing/packing_list.html",
        {
            "orders_with_totals": orders_with_totals,
            "total_products_sum": total_products_sum,
            "total_boxes_sum": total_boxes_sum,
        },
    )


@login_required
def packing_add_to_order(request, order_id):
    """Buyurtmaga yangi qadoqlash ma’lumotini qo‘shish"""
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        form = PackingForm(request.POST)
        if form.is_valid():
            packing = form.save(commit=False)
            packing.order = order
            packing.created_by = request.user
            packing.save()
            messages.success(request, "Qadoqlash ma’lumoti muvaffaqiyatli qo‘shildi!")
            return redirect("plm:plan_order_detail", order_id=packing.order.pk)
    else:
        form = PackingForm()

    return render(request, "planning/packing/packing_form.html", {"form": form, "order": order})


@login_required
def packing_update(request, pk):
    """Qadoqlash ma’lumotini tahrirlash"""
    packing = get_object_or_404(Packing, pk=pk)
    order = packing.order

    if request.method == "POST":
        form = PackingForm(request.POST, instance=packing)
        if form.is_valid():
            form.save()
            messages.success(request, "Qadoqlash ma’lumoti yangilandi!")
            return redirect("plm:plan_order_detail", order_id=packing.order.pk)
    else:
        form = PackingForm(instance=packing)

    return render(request, "planning/packing/packing_form.html", {"form": form, "order": order})


@login_required
def packing_delete(request, pk):
    """Qadoqlash ma’lumotini o‘chirish"""
    packing = get_object_or_404(Packing, pk=pk)
    if request.method == "POST":
        packing.delete()
        messages.success(request, "Qadoqlash ma’lumoti o‘chirildi!")
        return redirect("plm:plan_order_detail", order_id=packing.order.pk)

    return render(request, "planning/packing/packing_confirm_delete.html", {"packing": packing})



@login_required
def shipment_list(request):
    """
    Tasdiqlangan buyurtmalar uchun yuklamalar ro‘yxati.
    Har bir buyurtma bo‘yicha jami yuklangan mahsulotlar va karopkalar sonini hisoblaydi.
    """
    confirmed_orders = (
        Order.objects.filter(
            id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
        )
        .prefetch_related("shipments")
        .order_by("-created_at")
    )

    orders_with_totals = []
    total_products_sum = 0
    total_boxes_sum = 0

    for order in confirmed_orders:
        shipments = order.shipments.all()
        product_quantity = shipments.aggregate(total=Sum("product_quantity"))["total"] or 0
        box_quantity = shipments.aggregate(total=Sum("box_quantity"))["total"] or 0

        total_products_sum += product_quantity
        total_boxes_sum += box_quantity

        orders_with_totals.append({
            "order": order,
            "product_quantity": product_quantity,
            "box_quantity": box_quantity,
        })

    context = {
        "orders_with_totals": orders_with_totals,
        "total_products_sum": total_products_sum,
        "total_boxes_sum": total_boxes_sum,
    }
    return render(request, "planning/shipment/shipment_list.html", context)



@login_required
def shipment_add_to_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = ShipmentForm(request.POST, request.FILES)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.order = order
            shipment.created_by = request.user
            shipment.save()
            messages.success(request, "Yuk muvaffaqiyatli qo‘shildi ✅")
            return redirect("plm:plan_order_detail", order_id=shipment.order.pk)
    else:
        form = ShipmentForm(initial={"order": order})
    return render(request, "planning/shipment/shipment_form.html", {"form": form, "order": order})


@login_required
def shipment_update(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    if request.method == "POST":
        form = ShipmentForm(request.POST, request.FILES, instance=shipment)
        if form.is_valid():
            form.save()
            messages.success(request, "Yuklama ma’lumoti yangilandi ✅")
            return redirect("plm:plan_order_detail", order_id=shipment.order.pk)
    else:
        form = ShipmentForm(instance=shipment)
    return render(request, "planning/shipment/shipment_form.html", {"form": form, "shipment": shipment})


@login_required
def shipment_delete(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)

    if request.method == "POST":
        order_id = shipment.order.id
        shipment.delete()
        messages.warning(request, "Yuk ma’lumoti o‘chirildi ❌")
        return redirect("plm:plan_order_detail", order_id=shipment.order.pk)

    return render(request, "planning/shipment/shipment_confirm_delete.html", {"shipment":shipment})


def test(request):
    return render(request, "planning/order_detailed.html")




@login_required
def plan_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)


    # Kesim (Cutting) bo‘yicha jami pastal
    cuttings = Cutting.objects.filter(order=order)
    jami_pastal = cuttings.aggregate(total=Sum("pastal_soni"))["total"] or 0

    prints = Printing.objects.filter(order=order)
    jami_pechat = sum(c.quantity for c in order.prints.all())

    # ✅ Tikim (Stitching) — stitching_list logikasi asosida
    order_size_totals = defaultdict(int)
    total_quantity = 0

    for ordersize in order.ordersize.all():
        stitched_sum = ordersize.stitchings.aggregate(total=Sum("quantity"))["total"] or 0
        order_size_totals[ordersize.size] += stitched_sum
        total_quantity += stitched_sum

    ironing = Ironing.objects.filter(order=order)
    jami_dazmol = sum(c.quantity for c in order.ironing.all())

    # ✅ Sifat nazorati (Inspection) umumiy statistika
    inspections = Inspection.objects.filter(order=order)
    total_checked = inspections.aggregate(total=Sum("total_checked"))["total"] or 0
    total_passed = inspections.aggregate(total=Sum("passed_quantity"))["total"] or 0
    total_failed = inspections.aggregate(total=Sum("failed_quantity"))["total"] or 0

    # Qadoqlash
    packings = Packing.objects.filter(order=order)
    total_packed_products = packings.aggregate(total=Sum("product_quantity"))["total"] or 0
    total_boxes = packings.aggregate(total=Sum("box_quantity"))["total"] or 0

    # Yuklama
    shipment = Shipment.objects.filter(order=order)
    total_shipment_products = shipment.aggregate(total=Sum("product_quantity"))["total"] or 0
    total_shipment_box = shipment.aggregate(total=Sum("box_quantity"))["total"] or 0



    context = {
        "order": order,
        "fabrics": FabricArrival.objects.filter(order=order),
        "accessories": Accessory.objects.filter(order=order),

        "cuttings": cuttings,
        "jami_pastal": jami_pastal,

        "prints": prints,
        "jami_pechat": jami_pechat,

        "stitchings": Stitching.objects.filter(ordersize__order=order),
        "order_size_totals": dict(order_size_totals),
        "order_total_quantity": total_quantity,

        # "classifications": Classification.objects.filter(order=order),
        "ironings": ironing,
        "jami_dazmol": jami_dazmol,

        "inspections": inspections,
        "total_checked": total_checked,
        "total_passed": total_passed,
        "total_failed": total_failed,

        "packings": packings,
        "total_packed_products": total_packed_products,
        "total_boxes": total_boxes,

        "shipment": shipment,
        "total_shipment_products": total_shipment_products,
        "total_shipment_box": total_shipment_box,

        # "shipments": Shipment.objects.filter(order=order),
    }
    return render(request, "planning/order_detailed.html", context)






































































