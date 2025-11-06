import os
from django.core.files.storage import Storage
from imagekitio import ImageKit


class ImageKitStorage(Storage):
    def __init__(self):
        self.imagekit = ImageKit(
            private_key=os.getenv('IMAGEKIT_PRIVATE_KEY'),
            public_key=os.getenv('IMAGEKIT_PUBLIC_KEY'),
            url_endpoint=os.getenv('IMAGEKIT_URL_ENDPOINT')
        )

    def _save(self, name, content):
        # 🔹 Faylni ImageKit’ga yuklash
        upload = self.imagekit.upload_file(
            file=content,
            file_name=name,
        )

        # ✅ upload.url — bu haqiqiy ImageKit havolasi
        # Django modelga URL emas, faqat fayl nomini yozadi
        # URL esa .url() metodida qaytariladi
        return upload.name or name

    def url(self, name):
        # 🔹 To‘liq ImageKit URL qaytadi
        return f"{os.getenv('IMAGEKIT_URL_ENDPOINT').rstrip('/')}/{name.lstrip('/')}"

    def exists(self, name):
        # 🔹 Django fayl allaqachon bor deb o‘ylamasin
        return False
