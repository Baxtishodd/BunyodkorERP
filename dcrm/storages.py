import os
from io import BytesIO
from django.core.files.storage import Storage
from imagekitio import ImageKit


class ImageKitStorage(Storage):
    def __init__(self):
        self.imagekit = ImageKit(
            private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
            public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
            url_endpoint=os.getenv("IMAGEKIT_URL_ENDPOINT"),
        )

    def _save(self, name, content):
        """
        Faylni ImageKit'ga yuklash.
        Agar content bo'lmasa yoki None bo'lsa, mavjud fayl nomini qaytaradi.
        """
        # ⚙️ 1. Agar fayl None yoki bo‘sh bo‘lsa — mavjud nomni qaytaramiz
        if content is None:
            return name or ""

        # ⚙️ 2. Fayl nomi yo‘q bo‘lsa, content.name dan olamiz
        if not name:
            name = getattr(content, "name", "unnamed_file")

        # ⚙️ 3. Faylni o‘qish (yopilgan bo‘lsa, ochib o‘qiymiz)
        try:
            file_data = content.read()
            if not file_data:  # Ba’zi holatlarda fayl bo‘sh bo‘ladi
                content.open()
                file_data = content.read()
        except Exception as e:
            print("⚠️ Faylni o‘qishda xato:", e)
            return name  # Xato bo‘lsa, mavjud nomni qaytaradi

        # ⚙️ 4. Faylni ImageKit'ga yuklash
        try:
            upload = self.imagekit.upload_file(
                file=BytesIO(file_data),
                file_name=name,
            )
        except Exception as e:
            print("⚠️ ImageKit yuklashda xato:", e)
            return name  # Yuklash xato bo‘lsa, nomni qaytaradi

        # ⚙️ 5. Django uchun saqlanadigan nomni qaytarish
        uploaded_name = getattr(upload, "name", None)
        return uploaded_name or name

    def url(self, name):
        """To‘liq URL qaytaradi"""
        if not name:
            return ""
        endpoint = os.getenv("IMAGEKIT_URL_ENDPOINT", "").rstrip("/")
        return f"{endpoint}/{name.lstrip('/')}"

    def exists(self, name):
        """Django faylni mavjud deb hisoblamasligi uchun"""
        return False
