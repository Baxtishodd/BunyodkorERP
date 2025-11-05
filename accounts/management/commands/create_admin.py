# accounts/management/commands/create_admin.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = "Create an admin (superuser) account automatically if it doesn't exist."

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

        # qo‘shimcha optional ma'lumotlar (xohlasangiz .env orqali ham berishingiz mumkin)
        phone = os.environ.get("DJANGO_SUPERUSER_PHONE", "")
        job_role = os.environ.get("DJANGO_SUPERUSER_JOBROLE", "Administrator")

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            user.job_role = job_role
            user.phone = phone
            user.save()
            self.stdout.write(self.style.SUCCESS(f"✅ Superuser '{username}' created successfully!"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ Superuser '{username}' already exists."))


# pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py create_admin