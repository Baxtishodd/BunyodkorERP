from django.urls import path
from . import views

app_name = "plm"

urlpatterns = [
    path("products/models/", views.productmodel_list, name="productmodel_list"),
    path("products/models/create/", views.productmodel_create, name="productmodel_create"),
    path("products/models/<int:pk>/", views.productmodel_detail, name="productmodel_detail"),
    path("products/models/<int:pk>/update/", views.productmodel_update, name="productmodel_update"),
    path("products/models/<int:pk>/delete/", views.productmodel_delete, name="productmodel_delete"),


]
