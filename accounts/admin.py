from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email','username','first_name','last_name','is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'profile_picture',
            'birthday',
            'job_role',
            'address',
            'phone',
            'mobile',
            'website',
            'whatsapp',
            'telegram',
        )}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)


