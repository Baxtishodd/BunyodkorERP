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
        upload = self.imagekit.upload_file(
            file=content,
            file_name=name,
        )
        return upload['name']

    def url(self, name):
        return f"{os.getenv('IMAGEKIT_URL_ENDPOINT')}/{name}"

    def exists(self, name):
        # Fayl nomi bilan to‘qnashuv bo‘lmasligi uchun
        return False
