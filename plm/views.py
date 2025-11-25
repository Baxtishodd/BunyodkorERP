from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProductModel, Printing
from .forms import (ProductModelForm, EmployeeForm, OrderForm, WorkTypeForm, FabricArrivalForm, AccessoryForm,
                    CuttingForm, PrintForm, OrderSizeForm, StitchingForm, IroningForm, PackingForm, InspectionForm,
                    ShipmentForm, ShipmentInvoiceForm, ShipmentItemForm, ClassificationForm, ModelAssignedForm,
                    ProductionLineForm, ChangeLogForm)

from .models import (ProductionLine, Employee, HourlyWork, WorkType, Order, FabricArrival, Accessory, ModelAssigned,
                     Cutting, OrderSize, Stitching, Ironing, Packing, Shipment, ShipmentInvoice, Inspection,
                     ShipmentItem, Classification, ChangeLog)
from django.shortcuts import render, redirect
from datetime import time
from django.utils import timezone

from django.contrib import messages
from django.db.models import Sum, Q, F
from collections import Counter, defaultdict
from django.core.paginator import Paginator

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

# @login_required
# def employee_list(request):
#     employees = Employee.objects.select_related("line").all()
#     return render(request, "employee/employee_list.html", {"employees": employees})


@login_required
def employee_list(request):
    # 🔍 Qidiruv so‘rovi
    search_query = request.GET.get("q", "").strip()

    # 📄 Har sahifada nechta xodim ko‘rsatish
    try:
        per_page = int(request.GET.get("per_page", 10))
    except (TypeError, ValueError):
        per_page = 10

    per_page_options = [5, 10, 25, 50, 100]

    # 🔹 Asosiy queryset
    employees = Employee.objects.select_related("line").order_by("-id")

    # 🔍 Qidiruv: ism familiya yoki patok nomi bo‘yicha
    if search_query:
        employees = employees.filter(
            Q(full_name__icontains=search_query) |
            Q(line__name__icontains=search_query)
        )

    # 📄 Pagination
    paginator = Paginator(employees, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # 📦 Kontekst
    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "per_page_options": per_page_options,
    }

    return render(request, "employee/employee_list.html", context)



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
            # 🔹 Tikilgan sonni Order model methodidan olish
            tikildi = order.total_stitched()
        else:
            artikul = None
            client = None
            order_id = None
            quantity = 0
            tikildi = 0

        # Progress
        progress = int((tikildi / quantity) * 100) if quantity else 0

        # Normativ (oxirgisi)
        norm = line.norm_set.last()
        daily_norm = norm.daily_norm if norm else 0
        hourly_norm = norm.hourly_norm if norm else 0

        # # Tikilgan mahsulot (masalan HourlyWork orqali)
        # tikildi = line.hourlywork_set.aggregate(total=Sum("quantity"))["total"] or 0
        #
        # # Progress % (tikilgan / umumiy reja)
        # progress = int((tikildi / quantity) * 100) if quantity else 0

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
    search_query = request.GET.get("q", "")
    sort_by = request.GET.get("sort", "created_at")
    direction = request.GET.get("dir", "desc")

    # 🔹 Dropdown filtrlar
    status_filter = request.GET.get("status")
    client_filter = request.GET.get("client")
    color_filter = request.GET.get("rangi")
    patok_filter = request.GET.get("patok")

    try:
        per_page = int(request.GET.get("per_page", 10))
    except (TypeError, ValueError):
        per_page = 10

    per_page_options = [5, 10, 25, 50, 100]

    orders = Order.objects.all().order_by("-created_at")

    # 🔍 Qidiruv
    if search_query:
        orders = orders.filter(
            Q(client__icontains=search_query)
            | Q(artikul__icontains=search_query)
            | Q(rangi__icontains=search_query)
        )

    # 🔽 Filtrlar
    if status_filter:
        orders = orders.filter(status=status_filter)
    if client_filter:
        orders = orders.filter(client=client_filter)
    if color_filter:
        orders = orders.filter(rangi=color_filter)
    if patok_filter:
        orders = orders.filter(modelassigned__line__id=patok_filter)




        # ⬆️⬇️ Sortirovka
    sort_fields = {
        "client": "client",
        "artikul": "artikul",
        "rangi": "rangi",
        "patok": "modelassigned__line__name",
        "created_at": "created_at",
    }

    if sort_by in sort_fields:
        sort_field = sort_fields[sort_by]
        if direction == "asc":
            orders = orders.order_by(sort_field)
        else:
            orders = orders.order_by(f"-{sort_field}")

    # 📄 Pagination
    paginator = Paginator(orders, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # 🔹 Dropdown variantlar
    status_choices = Order.STATUS_CHOICES
    client_choices = Order.objects.values_list("client", flat=True).distinct()
    color_choices = Order.objects.values_list("rangi", flat=True).distinct()
    patok_choices = ProductionLine.objects.all()


    return render(
        request,
        "orders/order_list.html",
        {
            "page_obj": page_obj,
            "search_query": search_query,
            "per_page": per_page,
            "per_page_options": per_page_options,
            "sort_by": sort_by,
            "direction": direction,
            # 🔽 filtrlar
            "status_choices": status_choices,
            "client_choices": client_choices,
            "color_choices": color_choices,
            "patok_choices": patok_choices,
            "status_filter": status_filter,
            "client_filter": client_filter,
            "color_filter": color_filter,
            "patok_filter": patok_filter,
        },
    )


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
        print("📂 Yuklangan fayllar:", request.FILES)
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


# @login_required
# def ordersize_delete(request, pk):
#     ordersize = get_object_or_404(OrderSize, pk=pk)
#     order = ordersize.order
#
#     if request.method == "POST":
#         ordersize.delete()
#         messages.success(request, "Buyurtma o'lchami muvaffaqiyatli o‘chirildi ✅")
#         return redirect("plm:order_detail", pk=order.pk)
#     return render(request, "orders/ordersize/ordersize_confirm_delete.html", {"ordersize": ordersize})

@login_required
def ordersize_delete(request, pk):
    ordersize = get_object_or_404(OrderSize, pk=pk)
    order = ordersize.order

    if request.method == "POST":
        # Tikim mavjudligini tekshiramiz
        if ordersize.stitchings.exists():
            messages.warning(request, "Ushbu o‘lcham tikim bilan bog‘langanligi sababli o‘chirib bo‘lmaydi ⚠️")
            return redirect("plm:order_detail", pk=order.pk)

        # Agar tikim yo‘q bo‘lsa — xavfsiz o‘chiramiz
        ordersize.delete()
        messages.success(request, "Buyurtma o‘lchami muvaffaqiyatli o‘chirildi ✅")
        return redirect("plm:order_detail", pk=order.pk)

    return render(request, "orders/ordersize/ordersize_confirm_delete.html", {"ordersize": ordersize})



# Mato tastiqlanish Ro‘yxat
@login_required
def fabric_list(request):
    # 🔍 Qidiruv so‘rovi
    search_query = request.GET.get("q", "")
    # 📄 Har sahifada nechta element — foydalanuvchi tanloviga qarab
    per_page = int(request.GET.get("per_page", 10))

    # ✅ Faqat ModelAssigned orqali tasdiqlangan buyurtmalar
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    ).prefetch_related("fabric_arrival").order_by("-created_at")

    # 🔍 Agar foydalanuvchi qidiruv so‘rovini kiritgan bo‘lsa
    if search_query:
        confirmed_orders = confirmed_orders.filter(
            Q(client__icontains=search_query)
            | Q(artikul__icontains=search_query)
            | Q(rangi__icontains=search_query)
        )

    # 📄 Pagination (10 ta element har sahifada)
    paginator = Paginator(confirmed_orders, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "per_page_options": [5, 10, 25, 50, 100],
    }
    return render(request, "planning/fabric/fabric_list.html", context)


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
    # 🔍 Qidiruv
    search_query = request.GET.get("q", "")
    # 📄 Har sahifada nechta element ko‘rsatiladi
    per_page = int(request.GET.get("per_page", 10))

    # ✅ Faqat ModelAssigned orqali tasdiqlangan buyurtmalar
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    ).prefetch_related("accessories").order_by("-created_at")

    # 🔍 Qidiruv
    if search_query:
        confirmed_orders = confirmed_orders.filter(
            Q(client__icontains=search_query)
            | Q(artikul__icontains=search_query)
            | Q(rangi__icontains=search_query)
        )

    # 📄 Pagination
    paginator = Paginator(confirmed_orders, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "per_page_options": [5, 10, 25, 50, 100],  # ✅ Foydalanuvchi tanlovi uchun
    }
    return render(request, "planning/accessory/accessory_list.html", context)


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
    # 🔍 Qidiruv so‘rovi
    search_query = request.GET.get("q", "")
    # 📄 Foydalanuvchi belgilaydigan sahifa hajmi
    per_page = int(request.GET.get("per_page", 10))

    # ✅ Faqat ModelAssigned orqali tasdiqlangan buyurtmalar
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    ).prefetch_related("cuttings").order_by("-created_at")

    # 🔍 Qidiruv (mijoz yoki artikul bo‘yicha)
    if search_query:
        confirmed_orders = confirmed_orders.filter(
            Q(client__icontains=search_query) | Q(artikul__icontains=search_query)
        )

    # 📊 Har bir buyurtma uchun jami pastal sonini hisoblash
    orders_with_totals = []
    for order in confirmed_orders:
        jami_pastal = sum(c.pastal_soni for c in order.cuttings.all())
        orders_with_totals.append({
            "order": order,
            "jami_pastal": jami_pastal,
        })

    # 📄 Pagination
    paginator = Paginator(orders_with_totals, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Kontekst
    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "per_page_options": [5, 10, 25, 50, 100],
    }
    return render(request, "planning/cutting/cutting_list.html", context)


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
            messages.success(request, "Kesim ma'lumoti muvaffaqiyatli qo‘shildi ✅")
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
    # 🔍 Qidiruv
    search_query = request.GET.get("q", "")
    # 📄 Foydalanuvchi tanlaydigan sahifa hajmi
    per_page = int(request.GET.get("per_page", 10))

    # ✅ Faqat ModelAssigned orqali tasdiqlangan buyurtmalar
    confirmed_orders = (
        Order.objects.filter(
            id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
        )
        .prefetch_related("prints")
        .order_by("-created_at")
    )

    # 🔍 Qidiruv — mijoz yoki artikul bo‘yicha
    if search_query:
        confirmed_orders = confirmed_orders.filter(
            Q(client__icontains=search_query)
            | Q(artikul__icontains=search_query)
        )

    # 📊 Har bir buyurtma uchun jami pechat miqdorini hisoblash
    orders_with_totals = []
    for order in confirmed_orders:
        jami_print = order.prints.aggregate(total=Sum("quantity"))["total"] or 0
        orders_with_totals.append({
            "order": order,
            "jami_print": jami_print,
        })

    # 📄 Pagination
    paginator = Paginator(orders_with_totals, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # 📦 Context
    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "per_page_options": [5, 10, 25, 50, 100],
    }
    return render(request, "planning/print/print_list.html", context)

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


# @login_required
# def stitching_list(request):
#     confirmed_orders = (
#         Order.objects.filter(
#             id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
#         )
#         .prefetch_related("ordersize__stitchings")
#         .order_by("created_at")
#     )
#
#     # Har bir order uchun jami tikilgan o‘lchamlar lug‘ati
#     order_size_totals = {}
#     order_total_quantity = {}
#
#     for order in confirmed_orders:
#         size_totals = defaultdict(int)
#         total_quantity = 0
#
#         for ordersize in order.ordersize.all():
#             stitched_sum = ordersize.stitchings.aggregate(total=Sum("quantity"))["total"] or 0
#             size_totals[ordersize.size] += stitched_sum
#             total_quantity += stitched_sum
#
#         order_size_totals[order.id] = dict(size_totals)
#         order_total_quantity[order.id] = total_quantity
#
#     return render(
#         request,
#         "planning/stitching/stitching_list.html",
#         {
#             "orders": confirmed_orders,
#             "order_size_totals": order_size_totals,
#             "order_total_quantity": order_total_quantity,
#         },
#     )

from collections import defaultdict

@login_required
def stitching_list(request):
    # GET parametrlar
    search_query = request.GET.get("q", "").strip()
    try:
        per_page = int(request.GET.get("per_page", 10))
    except (TypeError, ValueError):
        per_page = 10

    # Ruxsat etilgan per_page variantlari
    per_page_options = [5, 10, 25, 50, 100]
    if per_page not in per_page_options:
        per_page = 10

    # Asosiy queryset — ModelAssigned orqali tasdiqlangan buyurtmalar
    confirmed_orders_qs = (
        Order.objects.filter(
            id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
        )
        .prefetch_related("ordersize__stitchings")  # <-- e'tibor shu yerga: ordersize__stitchings
        .order_by("-created_at")
    )

    # Qidiruv: mijoz yoki artikul
    if search_query:
        confirmed_orders_qs = confirmed_orders_qs.filter(
            Q(client__icontains=search_query) | Q(artikul__icontains=search_query)
        )

    # Pagination — avval querysetni sahifalab olamiz
    paginator = Paginator(confirmed_orders_qs, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Faqat hozirgi sahifadagi buyurtmalar uchun jami hisob-kitoblarni qilamiz
    order_size_totals = {}     # { order_id: { size: total_for_that_size, ... }, ... }
    order_total_quantity = {}  # { order_id: total_quantity_for_order, ... }

    for order in page_obj.object_list:
        size_totals = defaultdict(int)
        total_quantity = 0

        # ordersize — OrderSize modeliga tegishli related_name (models.py ga mos)
        for ordersize in order.ordersize.all():
            # Har bir ordersize uchun stitchings (related_name="stitchings") bo'yicha yig'adigan summa
            stitched_sum = ordersize.stitchings.aggregate(total=Sum("quantity"))["total"] or 0
            size_totals[ordersize.size] += stitched_sum
            total_quantity += stitched_sum

        order_size_totals[order.id] = dict(size_totals)
        order_total_quantity[order.id] = total_quantity

    context = {
        "page_obj": page_obj,
        "order_size_totals": order_size_totals,
        "order_total_quantity": order_total_quantity,
        "search_query": search_query,
        "per_page": per_page,
        "per_page_options": per_page_options,
    }

    return render(request, "planning/stitching/stitching_list.html", context)


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
            messages.success(request, "Tikimga ish qo'shildi! ✅")
            return redirect("plm:plan_order_detail", order_id=order.pk)
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
            return redirect("plm:plan_order_detail", order_id=order.pk)
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
        messages.success(request, "Tikim yozuvi muvaffaqiyatli o‘chirildi ✅")
        return redirect("plm:plan_order_detail", order_id=order.pk)

    return render(request, "planning/stitching/stitching_confirm_delete.html", {"stitching": stitching})



# ironing view Dazmol modeli
@login_required
def ironing_list(request):
    # 🔍 Qidiruv va sahifalash parametrlari
    search_query = request.GET.get("q", "").strip()
    try:
        per_page = int(request.GET.get("per_page", 10))
    except (TypeError, ValueError):
        per_page = 10

    # Ruxsat etilgan variantlar
    per_page_options = [5, 10, 25, 50, 100]
    if per_page not in per_page_options:
        per_page = 10

    # ✅ Faqat ModelAssigned orqali tasdiqlangan buyurtmalar
    confirmed_orders = (
        Order.objects.filter(
            id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
        )
        .prefetch_related("ironing")
        .order_by("-created_at")
    )

    # 🔍 Qidiruv — mijoz, artikul yoki rang bo‘yicha
    if search_query:
        confirmed_orders = confirmed_orders.filter(
            Q(client__icontains=search_query)
            | Q(artikul__icontains=search_query)
            | Q(rangi__icontains=search_query)
        )

    # 📊 Har bir buyurtma uchun jami dazmol miqdorini hisoblash
    orders_with_totals = []
    for order in confirmed_orders:
        jami_dazmol = order.ironing.aggregate(total=Sum("quantity"))["total"] or 0
        orders_with_totals.append({
            "order": order,
            "jami_dazmol": jami_dazmol,
        })

    # 📄 Pagination
    paginator = Paginator(orders_with_totals, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # 📦 Context
    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "per_page_options": per_page_options,
    }

    return render(request, "planning/ironing/ironing_list.html", context)





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
            messages.success(request, "Dazmol ma'lumoti yangilandi!")
            return redirect("plm:plan_order_detail", order_id=ironing_obj.order.pk)
    else:
        form = IroningForm(instance=ironing_obj)
    return render(request, 'planning/ironing/ironing_form.html', {'form': form, 'order': order})

@login_required
def ironing_delete(request, pk):
    ironing = get_object_or_404(Ironing, pk=pk)
    if request.method == 'POST':
        ironing.delete()
        messages.success(request, "Dazmol ma'lumoti o‘chirildi ❌")
        return redirect("plm:plan_order_detail", order_id=ironing.order.pk)
    return render(request, 'planning/ironing/ironing_confirm_delete.html', {'ironing': ironing})


# Inspection VIEW
@login_required
def inspection_list(request):
    search_query = request.GET.get("q", "").strip()

    # 📄 Har sahifada nechta element chiqishi
    try:
        per_page = int(request.GET.get("per_page", 10))
    except (TypeError, ValueError):
        per_page = 10

    per_page_options = [5, 10, 25, 50, 100]

    # 🔹 Faqat model tayinlangan (tasdiqlangan) buyurtmalar
    confirmed_orders = (
        Order.objects.filter(modelassigned__isnull=False)
        .prefetch_related("inspections", "ordersize")
        .order_by("-created_at")
        .distinct()
    )

    # 🔍 Qidiruv
    if search_query:
        confirmed_orders = confirmed_orders.filter(
            Q(artikul__icontains=search_query) | Q(client__icontains=search_query)
        )

    # 🔹 Hisob-kitoblar
    data = []
    for order in confirmed_orders:
        total_order_qty = order.sum_order_size() or 0  # buyurtmadagi umumiy son
        inspections = order.inspections.all()

        total_passed = inspections.aggregate(s=Sum("passed_quantity"))["s"] or 0
        total_failed = inspections.aggregate(s=Sum("failed_quantity"))["s"] or 0
        total_checked = total_passed + total_failed

        passed_percent = round((total_passed / total_order_qty * 100), 1) if total_order_qty else 0

        data.append({
            "order": order,
            "client": order.client,
            "artikul": order.artikul,
            "model_picture": order.model_picture.url if order.model_picture else None,
            "total_order_qty": total_order_qty,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_checked": total_checked,
            "passed_percent": passed_percent,
        })

    # 📄 Pagination
    paginator = Paginator(data, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "data": data,
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "per_page_options": per_page_options,
    }

    return render(request, "planning/inspection/inspection_list.html", context)

# -

@login_required
def inspection_add_to_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        form = InspectionForm(request.POST)
        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.order = order
            inspection.created_by = request.user
            inspection.inspection_date = timezone.now()
            inspection.save()

            messages.success(request, "✅ Sifat nazorati ma’lumoti muvaffaqiyatli qo‘shildi!")
            return redirect("plm:plan_order_detail", order_id=order.id)
    else:
        form = InspectionForm()

    context = {
        "order": order,
        "form": form,
        "title": f"{order.artikul} uchun Inspection qo‘shish",
    }
    return render(request, "planning/inspection/inspection_form.html", context)


@login_required
def inspection_update(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    order = inspection.order

    if request.method == "POST":
        form = InspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            messages.success(request, "Sifat nazorati ma’lumoti yangilandi ✅")
            return redirect("plm:plan_order_detail", order_id=order.id)
    else:
        form = InspectionForm(instance=inspection)

    return render(
        request,
        "planning/inspection/inspection_form.html",
        {"form": form, "order": order},
    )

@login_required
def inspection_delete(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    order = inspection.order

    if request.method == "POST":
        inspection.delete()
        messages.success(request, "Sifat nazorati yozuvi o‘chirildi ❌")
        return redirect("plm:plan_order_detail", order_id=order.id)

    return render(
        request,
        "planning/inspection/inspection_confirm_delete.html",
        {"inspection": inspection, "order": order},
    )


# Packing VIEW
@login_required
def packing_list(request):
    # 🔍 Qidiruv va sahifalash
    search_query = request.GET.get("q", "").strip()
    try:
        per_page = int(request.GET.get("per_page", 10))
    except (TypeError, ValueError):
        per_page = 10

    per_page_options = [5, 10, 25, 50, 100]
    if per_page not in per_page_options:
        per_page = 10

    # ✅ Faqat tasdiqlangan buyurtmalar
    confirmed_orders = (
        Order.objects.filter(modelassigned__isnull=False)
        .prefetch_related("packings")
        .order_by("-created_at")
        .distinct()
    )

    # 🔍 Qidiruv (mijoz, artikul, rang)
    if search_query:
        confirmed_orders = confirmed_orders.filter(
            Q(client__icontains=search_query)
            | Q(artikul__icontains=search_query)
            | Q(rangi__icontains=search_query)
        )

    # 📊 Har bir buyurtma uchun jami qadoqlash
    orders_with_totals = []
    for order in confirmed_orders:
        packings = order.packings.all()
        jami_box = packings.aggregate(total=Sum("box_quantity"))["total"] or 0
        jami_product = packings.aggregate(total=Sum("product_quantity"))["total"] or 0

        orders_with_totals.append({
            "order": order,
            "jami_box": jami_box,
            "jami_product": jami_product,
        })

    # 📄 Pagination
    paginator = Paginator(orders_with_totals, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "per_page_options": per_page_options,
    }

    return render(request, "planning/packing/packing_list.html", context)





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
    inspections = order.inspections.all().order_by("-inspection_date")

    total_order = order.sum_order_size() if hasattr(order, "sum_order_size") else 0
    total_checked = sum(i.passed_quantity + i.failed_quantity for i in inspections)
    total_passed = sum(i.passed_quantity for i in inspections)
    total_failed = sum(i.failed_quantity for i in inspections)

    passed_percentage = (
        round((total_passed / total_checked) * 100, 1)
        if total_checked else 0
    )

    # Qadoqlash
    packings = Packing.objects.filter(order=order)
    total_packed_products = packings.aggregate(total=Sum("product_quantity"))["total"] or 0
    total_boxes = packings.aggregate(total=Sum("box_quantity"))["total"] or 0

    # Yuklama
    shipment = Shipment.objects.filter(order=order)
    total_shipment_products = shipment.aggregate(total=Sum("product_quantity"))["total"] or 0
    total_shipment_box = shipment.aggregate(total=Sum("box_quantity"))["total"] or 0

    # ✅ TASnif (Classification)
    classifications = Classification.objects.filter(ordersize__order=order).select_related("ordersize", "created_by")

    total_first_sort = sum(c.first_sort for c in classifications)
    total_second_sort = sum(c.second_sort for c in classifications)
    total_defect = sum(c.defect for c in classifications)
    total_classified_all = total_first_sort + total_second_sort + total_defect



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

        "classifications": classifications,
        "total_first_sort": total_first_sort,
        "total_second_sort": total_second_sort,
        "total_defect": total_defect,
        "total_classified_all": total_classified_all,

        "ironings": ironing,
        "jami_dazmol": jami_dazmol,

        "inspections": inspections,
        "total_order": total_order,
        "total_checked": total_checked,
        "total_passed": total_passed,
        "total_failed": total_failed,
        "passed_percentage": passed_percentage,

        "packings": packings,
        "total_packed_products": total_packed_products,
        "total_boxes": total_boxes,

        "shipment": shipment,
        "total_shipment_products": total_shipment_products,
        "total_shipment_box": total_shipment_box,

        # "shipments": Shipment.objects.filter(order=order),
    }
    return render(request, "planning/order_detailed.html", context)


@login_required
def fabric_arrival_dashboard(request):
    # 1️⃣ Mato kelgan buyurtmalar
    confirmed_orders = (
        Order.objects.filter(
            id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
        )
        .prefetch_related("fabric_arrival")
        .order_by("-created_at")
    )

    # 2️⃣ Eng yaqin buyurtmalar (deadline bo‘yicha)
    upcoming_orders = Order.objects.filter(deadline__isnull=False).order_by("deadline")[:5]

    context = {
        "orders": confirmed_orders,
        "upcoming_orders": upcoming_orders,
    }
    return render(request, "planning/fabric/fabric_arrival_dashboard.html", context)


# Shipment Invoice CRUD


@login_required
def shipmentinvoice_list(request):
    """Yuk xatlari ro‘yxati"""
    search_query = request.GET.get("q", "")
    per_page = int(request.GET.get("per_page", 10))

    invoices = ShipmentInvoice.objects.all().order_by("-created_at")

    if search_query:
        invoices = invoices.filter(
            destination__icontains=search_query
        )

    paginator = Paginator(invoices, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "per_page_options": [5, 10, 25, 50, 100],
    }
    return render(request, "planning/shipmentinvoice/shipmentinvoice_list.html", context)


@login_required
def shipmentinvoice_create(request):
    """Yangi yuk xati qo‘shish"""
    if request.method == "POST":
        form = ShipmentInvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            messages.success(request, "Yangi yuk xati muvaffaqiyatli qo‘shildi ✅")
            return redirect("plm:shipmentinvoice_list")
    else:
        form = ShipmentInvoiceForm()

    return render(
        request,
        "planning/shipmentinvoice/shipmentinvoice_form.html",
        {"form": form},
    )


@login_required
def shipmentinvoice_update(request, pk):
    """Yuk xatini tahrirlash"""
    invoice = get_object_or_404(ShipmentInvoice, pk=pk)
    if request.method == "POST":
        form = ShipmentInvoiceForm(request.POST, request.FILES, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, "Yuk xati ma’lumoti yangilandi ✅")
            return redirect("plm:shipmentinvoice_list")
    else:
        form = ShipmentInvoiceForm(instance=invoice)

    return render(
        request,
        "planning/shipmentinvoice/shipmentinvoice_form.html",
        {"form": form, "invoice": invoice},
    )


@login_required
def shipmentinvoice_delete(request, pk):
    """Yuk xatini o‘chirish"""
    invoice = get_object_or_404(ShipmentInvoice, pk=pk)
    if request.method == "POST":
        invoice.delete()
        messages.success(request, "Yuk xati o‘chirildi ❌")
        return redirect("plm:shipmentinvoice_list")

    return render(
        request,
        "planning/shipmentinvoice/shipmentinvoice_confirm_delete.html",
        {"invoice": invoice},
    )



# Shipmentitem

@login_required
def shipment_items_list(request, shipment_id):
    shipment = get_object_or_404(ShipmentInvoice, id=shipment_id)
    items = shipment.items.select_related("order").all()

    # 📊 jami hisoblash
    total_quantity = sum(item.quantity for item in items)

    return render(request, "planning/shipmentitem/shipment_items_list.html", {
        "shipment": shipment,
        "items": items,
        "total_quantity": total_quantity,
    })


@login_required
def shipment_item_create(request, shipment_id):
    shipment = get_object_or_404(ShipmentInvoice, id=shipment_id)

    # ✅ faqat ModelAssigned orqali tasdiqlangan buyurtmalarni olish
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    )

    if request.method == "POST":
        form = ShipmentItemForm(request.POST)
    else:
        form = ShipmentItemForm()

    # ✅ form ichidagi order tanlovini faqat tasdiqlangan buyurtmalarga cheklaymiz
    if "order" in form.fields:
        form.fields["order"].queryset = confirmed_orders

    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.shipment = shipment  # avtomatik yuk xatiga biriktirish
        item.save()
        messages.success(request, "Yangi yuk tarkibi muvaffaqiyatli qo‘shildi ✅")
        return redirect("plm:shipment_items_list", shipment_id=shipment.id)

    return render(request, "planning/shipmentitem/shipment_item_form.html", {
        "form": form,
        "shipment": shipment,
    })




@login_required
def shipment_item_update(request, shipment_id, item_id):
    shipment = get_object_or_404(ShipmentInvoice, id=shipment_id)
    item = get_object_or_404(ShipmentItem, id=item_id, shipment=shipment)

    # ✅ faqat ModelAssigned orqali tasdiqlangan buyurtmalarni olish
    confirmed_orders = Order.objects.filter(
        id__in=ModelAssigned.objects.values_list("model_name_id", flat=True)
    )

    if request.method == "POST":
        form = ShipmentItemForm(request.POST, instance=item)
    else:
        form = ShipmentItemForm(instance=item)

    # ✅ formdagi order tanlovini faqat tastiqlangan buyurtmalarga cheklash
    if "order" in form.fields:
        form.fields["order"].queryset = confirmed_orders

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Yuk tarkibi yangilandi ✏️")
        return redirect("plm:shipment_items_list", shipment_id=shipment.id)

    return render(request, "planning/shipmentitem/shipment_item_form.html", {
        "form": form,
        "shipment": shipment,
    })


@login_required
def shipment_item_delete(request, shipment_id, pk):
    """Yuk tarkibini o‘chirish"""
    shipment = get_object_or_404(ShipmentInvoice, id=shipment_id)
    item = get_object_or_404(ShipmentItem, pk=pk, shipment=shipment)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Yuk tarkibi o‘chirildi ❌")
        return redirect("plm:shipment_items_list", shipment_id=shipment.id)

    context = {
        "shipment": shipment,
        "item": item,
    }
    return render(request, "planning/shipmentitem/shipment_item_confirm_delete.html", context)


@login_required
def classification_add_to_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    is_confirmed = ModelAssigned.objects.filter(model_name_id=order_id).exists()

    if not is_confirmed:
        messages.warning(request, "Bu buyurtma hali tasdiqlanmagan!")
        return redirect("plm:classification_list")

    if request.method == "POST":
        form = ClassificationForm(request.POST)
        if form.is_valid():
            classification = form.save(commit=False)
            classification.created_by = request.user
            classification.save()
            messages.success(request, "Razmer bo‘yicha tasnif muvaffaqiyatli qo‘shildi ✅")
            return redirect("plm:plan_order_detail", order_id=order.pk)
    else:
        # faqat shu buyurtmaga tegishli razmerlar chiqsin
        form = ClassificationForm()
        form.fields["ordersize"].queryset = OrderSize.objects.filter(order=order)

    return render(request, "planning/classification/classification_form.html", {
        "form": form,
        "order": order
    })


@login_required
def classification_list(request):
    # 🔍 Qidiruv
    search_query = request.GET.get("q", "").strip()
    try:
        per_page = int(request.GET.get("per_page", 10))
    except (TypeError, ValueError):
        per_page = 10

    # ✅ Faqat ModelAssigned orqali tasdiqlangan buyurtmalar
    confirmed_orders = (
        Order.objects.filter(modelassigned__isnull=False)
        .prefetch_related("ordersize__classifications")
        .order_by("-created_at")
        .distinct()
    )

    # 🔍 Qidiruv (mijoz yoki artikul bo‘yicha)
    if search_query:
        confirmed_orders = confirmed_orders.filter(
            Q(client__icontains=search_query) |
            Q(artikul__icontains=search_query)
        )

    # 📊 Hisob-kitoblar
    results = []
    for order in confirmed_orders:
        # Order ichidagi barcha classification yozuvlarini yig‘amiz
        totals = order.ordersize.all().aggregate(
            total_first=Sum("classifications__first_sort"),
            total_second=Sum("classifications__second_sort"),
            total_defect=Sum("classifications__defect"),
        )

        total_first = totals["total_first"] or 0
        total_second = totals["total_second"] or 0
        total_defect = totals["total_defect"] or 0
        total_all = total_first + total_second + total_defect
        first_percent = round((total_first / total_all) * 100, 2) if total_all else 0

        results.append({
            "order": order,
            "total_first": total_first,
            "total_second": total_second,
            "total_defect": total_defect,
            "total_all": total_all,
            "first_percent": first_percent,
        })

    # 📄 Pagination
    paginator = Paginator(results, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # 📦 Context
    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "per_page_options": [5, 10, 25, 50, 100],
    }

    return render(request, "planning/classification/classification_list.html", context)




@login_required
def classification_update(request, pk):
    classification = get_object_or_404(Classification, pk=pk)
    order = classification.ordersize.order  # Buyurtma bilan bog‘lash

    if request.method == "POST":
        form = ClassificationForm(request.POST, instance=classification)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.save()
            messages.success(request, "Tasnif ma’lumoti muvaffaqiyatli yangilandi ✅")
            return redirect("plm:plan_order_detail", order_id=order.pk)
        else:
            messages.error(request, "Xatolik yuz berdi. Ma’lumotni tekshirib qayta urinib ko‘ring.")
    else:
        form = ClassificationForm(instance=classification)

    return render(
        request,
        "planning/classification/classification_form.html",
        {"form": form, "order": order, "classification": classification},
    )


@login_required
def classification_delete(request, pk):
    classification = get_object_or_404(Classification, pk=pk)
    order = classification.ordersize.order  # buyurtma bilan bog‘lash

    if request.method == "POST":
        classification.delete()
        messages.success(request, "Tasnif muvaffaqiyatli o‘chirildi 🗑️")
        return redirect("plm:plan_order_detail", order_id=order.pk)

    return render(
        request,
        "planning/classification/classification_confirm_delete.html",
        {"classification": classification, "order": order},
    )


@login_required
def reglament_view(request):
    return render(request, "kodex/reglament.html")



from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date

@login_required
def modelassigned_list(request):
    """Biriktirilgan modellar ro‘yxati"""
    search_query = request.GET.get("q", "").strip()
    line_filter = request.GET.get("line", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    # Har sahifada nechta yozuv bo‘lishi
    try:
        per_page = int(request.GET.get("per_page", 10))
    except (ValueError, TypeError):
        per_page = 10

    # 🔹 Asosiy queryset
    assigned_list = (
        ModelAssigned.objects.select_related("line", "model_name")
        .order_by("-assigned_date")
    )

    # 🔍 Qidiruv
    if search_query:
        assigned_list = assigned_list.filter(
            Q(line__name__icontains=search_query)
            | Q(model_name__client__icontains=search_query)
            | Q(model_name__artikul__icontains=search_query)
        )

    # 🔽 Filtrlar
    if line_filter:
        assigned_list = assigned_list.filter(line_id=line_filter)

    if start_date:
        assigned_list = assigned_list.filter(assigned_date__gte=parse_date(start_date))
    if end_date:
        assigned_list = assigned_list.filter(assigned_date__lte=parse_date(end_date))

    # 📄 Pagination
    paginator = Paginator(assigned_list, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # 🔹 Patoklar ro‘yxati filtr uchun
    line_choices = ProductionLine.objects.all()

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "line_filter": line_filter,
        "start_date": start_date,
        "end_date": end_date,
        "per_page": per_page,
        "per_page_options": [5, 10, 25, 50, 100],
        "line_choices": line_choices,
    }

    return render(request, "planning/modelassigned/modelassigned_list.html", context)

@login_required
def modelassigned_create(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == "POST":
        form = ModelAssignedForm(request.POST)
        if form.is_valid():
            model_assigned = form.save(commit=False)
            model_assigned.model_name = order  # buyurtmani biriktiramiz
            model_assigned.save()
            messages.success(request, "Model patokka muvaffaqiyatli biriktirildi ✅")
            # Yoki shu patok sahifasiga qaytish
            return redirect("plm:productionline_detail", pk=model_assigned.line.pk)
    else:
        # Dastlab model tanlangan holda formni ochish
        form = ModelAssignedForm(initial={"model_name": order})

    return render(request, "planning/modelassigned/modelassigned_form.html", {"form": form, "order": order})


# @login_required
# def modelassigned_create(request, order_id=None):
#     """Buyurtma uchun modelni patokka biriktirish"""
#     order = None
#     if order_id:
#         order = get_object_or_404(Order, id=order_id)
#
#     if request.method == "POST":
#         form = ModelAssignedForm(request.POST)
#
#         if form.is_valid():
#             assigned = form.save(commit=False)
#
#             # Agar buyurtma urldan kelsa, formda model_name ni o‘zgartirmaymiz
#             if order:
#                 assigned.model_name = order
#
#             assigned.save()
#             messages.success(request, "✅ Model patokka muvaffaqiyatli biriktirildi!")
#             return redirect("plm:order_list")
#     else:
#         # formni buyurtma bilan oldindan to‘ldiramiz (disabled)
#         if order:
#             form = ModelAssignedForm(initial={"model_name": order})
#             form.fields["model_name"].disabled = True
#         else:
#             form = ModelAssignedForm()
#
#     context = {"form": form, "order": order}
#     return render(request, "planning/modelassigned/modelassigned_form.html", context)


@login_required
def modelassigned_delete(request, pk):
    """Biriktirilgan modelni o‘chirish"""
    assigned = get_object_or_404(ModelAssigned, pk=pk)

    if request.method == "POST":
        assigned.delete()
        messages.success(request, "Biriktirilgan model o‘chirildi ❌")
        return redirect("plm:modelassigned_list")

    context = {"assigned": assigned}
    return render(request, "planning/modelassigned/modelassigned_confirm_delete.html", context)


@login_required
def productionline_create(request):
    if request.method == 'POST':
        form = ProductionLineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangi patok muvaffaqiyatli qo‘shildi ✅")
            return redirect('plm:productionline_list')
    else:
        form = ProductionLineForm()
    return render(request, 'planning/line/productionline_form.html', {'form': form})


from itertools import groupby
@login_required
def changelog_list(request):
    changelogs = ChangeLog.objects.all().order_by("-created_at")

    grouped_logs = []
    for month, logs in groupby(changelogs, key=lambda x: x.created_at.strftime("%B %Y")):
        grouped_logs.append({
            "month": month,
            "logs": list(logs)
        })

    return render(request, "system/changelog_list.html", {"grouped_logs": grouped_logs})

@login_required
def changelog_create(request):
    if request.method == "POST":
        form = ChangeLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.author = request.user
            log.save()
            return redirect("plm:changelog_list")
    else:
        form = ChangeLogForm()
    return render(request, "system/changelog_form.html", {"form": form})

# =============== DASHBOARD PAGE ===============
from datetime import timedelta
from django.db.models import Count, Sum
from django.utils import timezone

@login_required
def dashboard(request):
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)

    # --- Umumiy ko‘rsatkichlar ---
    total_orders = Order.objects.count()
    active_orders = Order.objects.filter(status="in_production").count()
    completed_orders = Order.objects.filter(status="completed").count()
    total_lines = ProductionLine.objects.count()
    total_employees = Employee.objects.count()
    today_stitched = Stitching.objects.filter(date=today).aggregate(total=Sum("quantity"))["total"] or 0

    # --- Patoklar holati ---
    lines_data = []
    for line in ProductionLine.objects.all():
        employees_count = line.employee_count()
        assigned = line.modelassigned_set.last()
        if assigned:
            order = assigned.model_name
            artikul = order.artikul
            client = order.client
            tikildi = order.total_stitched()
            quantity = order.sum_order_size() or 0
            progress = int((tikildi / quantity) * 100) if quantity else 0
        else:
            artikul = client = None
            tikildi = quantity = progress = 0
        lines_data.append({
            "name": line.name,
            "client": client,
            "artikul": artikul,
            "employees": employees_count,
            "tikildi": tikildi,
            "quantity": quantity,
            "progress": progress
        })


    order_status_data = []
    status_counts = Order.objects.values("status").annotate(total=Count("id"))
    for s in status_counts:
        code = s["status"]
        label = dict(Order.STATUS_CHOICES).get(code, code)
        order_status_data.append({
            "status": code,  # chart rang uchun kerak
            "label": label,  # foydalanuvchiga ko‘rsatish uchun
            "total": s["total"]
        })

    # --- Eng faol ishchilar ---
    top_employees = (
        HourlyWork.objects.values("employee__full_name")
        .annotate(total=Sum("quantity"))
        .order_by("-total")[:5]
    )

    # --- Ishlab chiqarish bosqichlari statistikasi ---
    production_stats = {
        "cutting": Cutting.objects.aggregate(total=Sum("pastal_soni"))["total"] or 0,
        "printing": Printing.objects.aggregate(total=Sum("quantity"))["total"] or 0,
        "stitching": Stitching.objects.aggregate(total=Sum("quantity"))["total"] or 0,
        "ironing": Ironing.objects.aggregate(total=Sum("quantity"))["total"] or 0,
        "packing": Packing.objects.aggregate(total=Sum("product_quantity"))["total"] or 0,
    }

    # --- Deadline yaqinlashayotgan buyurtmalar ---
    urgent_orders = Order.objects.filter(
        deadline__lte=timezone.now() + timedelta(days=3),
        status__in=["new", "in_production"]
    ).order_by("deadline")[:10]

    context = {
        "total_orders": total_orders,
        "active_orders": active_orders,
        "completed_orders": completed_orders,
        "total_lines": total_lines,
        "total_employees": total_employees,
        "today_stitched": today_stitched,
        "lines_data": lines_data,
        "order_status_data": order_status_data,
        "top_employees": top_employees,
        "production_stats": production_stats,
        "urgent_orders": urgent_orders,
    }

    return render(request, "plm/dashboard.html", context)

































































