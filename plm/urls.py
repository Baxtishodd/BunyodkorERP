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

    path('worktypes/create/', views.worktype_create, name='worktype_create'),
    path("worktypes/", views.worktype_list, name="worktype_list"),

    path("production-lines/", views.productionline_list, name="productionline_list"),
    path("productionline/<int:pk>/", views.productionline_detail, name="productionline_detail"),

    path('fabrics/', views.fabric_list, name='fabric_list'),
    path('fabrics/create/', views.fabric_create, name='fabric_create'),
    path('fabrics/<int:pk>/confirm/', views.fabric_confirm, name='fabric_confirm'),
    path('fabrics/add/<int:order_id>/', views.fabric_add_to_order, name='fabric_add_to_order'),

    path('accessories/', views.accessory_list, name='accessory_list'),
    path('accessories/create/', views.accessory_create, name='accessory_create'),
    path('accessories/<int:pk>/edit/', views.accessory_update, name='accessory_update'),
    path('accessories/<int:pk>/delete/', views.accessory_delete, name='accessory_delete'),
    path('accessories/add/<int:order_id>/', views.accessory_add_to_order, name='accessory_add_to_order'),

    path('cuttings/', views.cutting_list, name='cutting_list'),
    path('cuttings/<int:pk>/edit/', views.cutting_update, name='cutting_update'),
    path('cuttings/<int:pk>/delete/', views.cutting_delete, name='cutting_delete'),
    path('cuttings/add/<int:order_id>/', views.cutting_add_to_order, name='cutting_add_to_order'),

    path('prints/', views.print_list, name='print_list'),
    # path('prints/create/', views.print_create, name='print_create'),
    path('prints/<int:pk>/edit/', views.print_update, name='print_update'),
    path('prints/<int:pk>/delete/', views.print_delete, name='print_delete'),
    path('prints/add/<int:order_id>/', views.print_add_to_order, name='print_add_to_order'),


    # Xodimlar
    path("employees/", views.employee_list, name="employee_list"),
    path('employees/add/', views.employee_create, name='employee_add'),




]
