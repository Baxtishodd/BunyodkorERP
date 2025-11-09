import os
import uuid
import requests
from django.core.files.storage import Storage
from django.core.files.base import ContentFile


class SupabaseStorage(Storage):
    """
    📦 Supabase Storage uchun maxsus backend.
    Har bir faylni UUID asosida unikal nom bilan yuklaydi.
    """

    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.anon_key = os.getenv("SUPABASE_ANON_KEY")
        self.bucket = os.getenv("SUPABASE_BUCKET", "media")

        self.api_url = f"{self.supabase_url}/storage/v1/object"
        self.public_url = f"{self.supabase_url}/storage/v1/object/public/{self.bucket}"

    def _save(self, name, content):
        """
        Faylni Supabase Storage'ga yuklaydi.
        Fayl nomi avtomatik ravishda UUID bilan unikal qilinadi.
        """
        try:
            ext = os.path.splitext(name)[1]  # masalan, .png yoki .jpg
            unique_name = f"{uuid.uuid4().hex}{ext}"
            name = f"orders/{unique_name}"

            headers = {
                "Authorization": f"Bearer {self.anon_key}",
                "apikey": self.anon_key,
                "Content-Type": "application/octet-stream",
            }

            if hasattr(content, "read"):
                data = content.read()
            elif isinstance(content, ContentFile):
                data = content.content
            else:
                raise TypeError("content formati noto‘g‘ri")

            upload_url = f"{self.api_url}/{self.bucket}/{name}?upsert=false"
            response = requests.put(upload_url, headers=headers, data=data, timeout=30)

            if response.status_code not in [200, 201]:
                raise Exception(f"Supabase upload xato: {response.status_code} - {response.text}")

            print(f"✅ Supabase’ga yuklandi: {name}")
            return name

        except Exception as e:
            print("❌ Supabase yuklashda xatolik:", str(e))
            raise

    def url(self, name):
        """Yuklangan fayl uchun to‘liq URL qaytaradi."""
        return f"{self.public_url}/{name}"

    def exists(self, name):
        """Django faylni mavjud deb hisoblamasligi uchun."""
        return False
