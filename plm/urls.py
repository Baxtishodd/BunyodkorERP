from django.urls import path
from . import views

app_name = "plm"

urlpatterns = [
    path("products/models/", views.productmodel_list, name="productmodel_list"),
    path("products/models/create/", views.productmodel_create, name="productmodel_create"),
    path("products/models/<int:pk>/", views.productmodel_detail, name="productmodel_detail"),
    path("products/models/<int:pk>/update/", views.productmodel_update, name="productmodel_update"),
    path("products/models/<int:pk>/delete/", views.productmodel_delete, name="productmodel_delete"),

    path("line/<int:line_id>/order/<int:order_id>/hourly-work/", views.hourly_work_table, name="hourly_work_table"),

    path("employees/", views.employee_list, name="employee_list"),
    path('employees/add/', views.employee_create, name='employee_add'),

    path("worktypes/", views.worktype_list, name="worktype_list"),

    path("production-lines/", views.productionline_list, name="productionline_list"),


]
