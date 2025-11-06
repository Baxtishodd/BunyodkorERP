import os
from django.core.files.storage import Storage
from imagekitio import ImageKit
from io import BytesIO

class ImageKitStorage(Storage):
    def __init__(self):
        self.imagekit = ImageKit(
            private_key=os.getenv('IMAGEKIT_PRIVATE_KEY'),
            public_key=os.getenv('IMAGEKIT_PUBLIC_KEY'),
            url_endpoint=os.getenv('IMAGEKIT_URL_ENDPOINT')
        )

    def _save(self, name, content):
        # ✅ Fayl nomini tekshirish
        if not name:
            name = getattr(content, 'name', 'unnamed_file')

        # ✅ Fayl obyektini o‘qish
        if hasattr(content, 'read'):
            file_data = content.read()
        else:
            raise ValueError("content obyektida read() metodi yo‘q!")

        # ✅ Faylni ImageKit’ga yuklash
        upload = self.imagekit.upload_file(
            file=BytesIO(file_data),
            file_name=name,
        )

        # ✅ Django model uchun faqat nomni saqlaymiz
        return upload.name or name

    def url(self, name):
        return f"{os.getenv('IMAGEKIT_URL_ENDPOINT').rstrip('/')}/{name.lstrip('/')}"

    def exists(self, name):
        return False
