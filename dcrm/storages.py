import os
import requests
from django.core.files.storage import Storage
from django.core.files.base import ContentFile


class SupabaseStorage(Storage):
    """
    Supabase Storage uchun fayl saqlovchi klass.
    Fayllarni Supabase bucket'ga yuklaydi va to‘liq public URL qaytaradi.
    """

    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.anon_key = os.getenv("SUPABASE_ANON_KEY")
        self.bucket = os.getenv("SUPABASE_BUCKET", "media")

        self.api_url = f"{self.supabase_url}/storage/v1/object"
        self.public_url = f"{self.supabase_url}/storage/v1/object/public/{self.bucket}"

        if not all([self.supabase_url, self.anon_key, self.bucket]):
            raise ValueError("Supabase sozlamalari to‘liq emas (.env faylni tekshiring)")

    def _save(self, name, content):
        """ Faylni Supabase'ga yuklash """
        try:
            headers = {
                "Authorization": f"Bearer {self.anon_key}",
                "apikey": self.anon_key,
                "Content-Type": "application/octet-stream",
            }

            # Fayl kontentini o‘qish
            if hasattr(content, "read"):
                data = content.read()
            elif isinstance(content, ContentFile):
                data = content.content
            else:
                raise TypeError("SupabaseStorage: content formati noto‘g‘ri")

            upload_url = f"{self.api_url}/{self.bucket}/{name}?upsert=true"

            # ⚡ Faylni PUT orqali yuborish
            response = requests.put(upload_url, headers=headers, data=data, timeout=30)

            # Agar xato bo‘lsa — log bilan chiqaramiz
            if response.status_code not in [200, 201]:
                raise Exception(
                    f"Supabase upload xato: {response.status_code} - {response.text}"
                )

            return name

        except Exception as e:
            print(f"⚠️ Supabase upload xatolik: {str(e)}")
            raise

    def url(self, name):
        """ Supabase public URL qaytaradi """
        return f"{self.public_url}/{name}"

    def exists(self, name):
        """ Django faylni o‘rniga yozsin deb har doim False """
        return False
