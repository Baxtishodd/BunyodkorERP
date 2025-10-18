from django.urls import path
from . import views
from .views import accessory_update

app_name = "plm"

urlpatterns = [
    path("products/models/", views.productmodel_list, name="productmodel_list"),
    path("products/models/create/", views.productmodel_create, name="productmodel_create"),
    path("products/models/<int:pk>/", views.productmodel_detail, name="productmodel_detail"),
    path("products/models/<int:pk>/update/", views.productmodel_update, name="productmodel_update"),
    path("products/models/<int:pk>/delete/", views.productmodel_delete, name="productmodel_delete"),

    # Model boshqaruvi
    path("line/<int:line_id>/order/<int:order_id>/hourly-work/", views.hourly_work_table, name="hourly_work_table"),

    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/edit/', views.order_update, name='order_update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

    # Order Plan
    path('plan/orders/<int:order_id>/', views.plan_order_detail, name='plan_order_detail'),

    path("ordersize/", views.ordersize_list, name="ordersize_list"),
    path("ordersize/<int:pk>/update/", views.ordersize_update, name="ordersize_update"),
    path("ordersize/<int:pk>/delete/", views.ordersize_delete, name="ordersize_delete"),
    path('ordersize/add/<int:pk>/', views.ordersize_add_to_order, name='ordersize_add_to_order'),

    path('worktypes/create/', views.worktype_create, name='worktype_create'),
    path("worktypes/", views.worktype_list, name="worktype_list"),

    path("production-lines/", views.productionline_list, name="productionline_list"),
    path("productionline/<int:pk>/", views.productionline_detail, name="productionline_detail"),

    path('fabrics/', views.fabric_list, name='fabric_list'),
    path('fabrics/<int:pk>/confirm/', views.fabric_confirm, name='fabric_confirm'),
    path('fabrics/add/<int:order_id>/', views.fabric_add_to_order, name='fabric_add_to_order'),
    path('fabrics/<int:pk>/edit/', views.fabric_update, name='fabric_update'),
    path('fabrics/<int:pk>/delete/', views.fabric_delete, name='fabric_delete'),
    path("fabric-arrival/dashboard/", views.fabric_arrival_dashboard, name="fabric_arrival_dashboard"),



    path('accessories/', views.accessory_list, name='accessory_list'),
    # path('accessories/create/', views.accessory_create, name='accessory_create'),
    path('accessories/<int:pk>/edit/', views.accessory_update, name='accessory_update'),
    path('accessories/<int:pk>/delete/', views.accessory_delete, name='accessory_delete'),
    path('accessories/add/<int:order_id>/', views.accessory_add_to_order, name='accessory_add_to_order'),

    path('cuttings/', views.cutting_list, name='cutting_list'),
    path('cuttings/<int:pk>/edit/', views.cutting_update, name='cutting_update'),
    path('cuttings/<int:pk>/delete/', views.cutting_delete, name='cutting_delete'),
    path('cuttings/add/<int:order_id>/', views.cutting_add_to_order, name='cutting_add_to_order'),

    path('prints/', views.print_list, name='print_list'),
    path('prints/<int:pk>/edit/', views.print_update, name='print_update'),
    path('prints/<int:pk>/delete/', views.print_delete, name='print_delete'),
    path('prints/add/<int:order_id>/', views.print_add_to_order, name='print_add_to_order'),

    path("stitchings/", views.stitching_list, name="stitching_list"),
    path("stitchings/add/<int:order_id>/", views.stitching_add, name="stitching_add"),
    path("stitchings/update/<int:pk>/", views.stitching_update, name="stitching_update"),
    path("stitchings/delete/<int:pk>/", views.stitching_delete, name="stitching_delete"),

    path('ironing/', views.ironing_list, name='ironing_list'),
    path('ironing/<int:pk>/edit/', views.ironing_update, name='ironing_update'),
    path('ironing/<int:pk>/delete/', views.ironing_delete, name='ironing_delete'),
    path('ironing/add/<int:order_id>/', views.ironing_add_to_order, name='ironing_add_to_order'),

    path("inspections/", views.inspection_list, name="inspection_list"),
    path('inspection/<int:pk>/edit/', views.inspection_update, name='inspection_update'),
    path("order/<int:order_id>/inspection/add/", views.inspection_add_to_order, name="inspection_add_to_order"),
    path("inspection/<int:pk>/delete/", views.inspection_delete, name="inspection_delete"),

    path("packing/", views.packing_list, name="packing_list"),
    path("packing/add/<int:order_id>/", views.packing_add_to_order, name="packing_add_to_order"),
    path("packing/update/<int:pk>/", views.packing_update, name="packing_update"),
    path("packing/delete/<int:pk>/", views.packing_delete, name="packing_delete"),

    path("shipment/list/", views.shipment_list, name="shipment_list"),
    path("shipment/add/<int:order_id>/", views.shipment_add_to_order, name="shipment_add_to_order"),
    path("shipment/update/<int:pk>/", views.shipment_update, name="shipment_update"),
    path("shipment/delete/<int:pk>/", views.shipment_delete, name="shipment_delete"),

    path("shipmentinvoice/list/", views.shipmentinvoice_list, name="shipmentinvoice_list"),
    path("shipmentinvoice/add/", views.shipmentinvoice_create, name="shipmentinvoice_create"),
    path("shipmentinvoice/<int:pk>/edit/", views.shipmentinvoice_update, name="shipmentinvoice_update"),
    path("shipmentinvoice/<int:pk>/delete/", views.shipmentinvoice_delete, name="shipmentinvoice_delete"),

    # Shipment item URLs (har bir yuk xatiga bog‘liq)
    path("shipment/<int:shipment_id>/items/", views.shipment_items_list, name="shipment_items_list"),
    path("shipment/<int:shipment_id>/items/add/", views.shipment_item_create, name="shipment_item_create"),
    path("shipment/<int:shipment_id>/items/<int:item_id>/edit/", views.shipment_item_update, name="shipment_item_update"),
    path("shipment/<int:shipment_id>/items/<int:pk>/delete/", views.shipment_item_delete, name="shipment_item_delete"),




    # Xodimlar
    path("employees/", views.employee_list, name="employee_list"),
    path('employees/add/', views.employee_create, name='employee_add'),

    path('test', views.test, name='test'),




]
