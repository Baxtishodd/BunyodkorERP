from django.urls import path
from .views import SignUpView
from . import views

app_name = "accounts"
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]