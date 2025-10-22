from django.urls import path
from . import views
from .views import AccountListView


urlpatterns = [
    path('', views.index_page, name='index'), # home page

    path('records', views.records_view, name='records'), # record list
    path('record/<int:pk>', views.customer_record, name='record'), # special detailed view
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),

    path('contact-list', views.contact_list, name='contact_list'),
    path('new-contact/', views.contact_create, name='contact_create'),
    path('edit-contact/<int:pk>/', views.contact_edit, name='contact_edit'),
    path('delete-contact/<int:pk>', views.contact_delete, name='contact_delete'),

    path('new-account/', views.account_create, name='account_create'),
    path('accounts/', AccountListView.as_view(), name='account_list'),

    path('requisition_create/', views.requisition_create, name='requisition_create'),
    path('requisition_list/', views.requisition_list, name='requisition_list'),

    path('payments/', views.payment_list, name='payment_list'),
    path('payments/create', views.create_payment, name='create_payment'),
    path('payments/<int:pk>/delete/', views.delete_payment, name='delete_payment'),
    path('payments/<int:pk>/edit/', views.edit_payment, name='edit_payment'),

    # path("export-income-payments/", views.export_income_payments_excel, name="export_income_payments"),
    path("export-income-payments/", views.export_payments_excel, name="export_income_payments"),


    path('dashboard/', views.dashboard_view, name='dashboard'),

]
