from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('register/', views.register_user, name='register'),

    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),


    path('products/', views.products, name='products'),
    path('product/<int:pk>', views.product_record, name='product'),
    path('delete_product/<int:pk>', views.delete_product, name='delete_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<int:pk>', views.update_product, name='update_product'),

    path('dashboard/', views.dashboard_view, name='dashboard'),

]
