import os
from io import BytesIO
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from imagekitio import ImageKit

# Optional: oson tekshiruv uchun
DEBUG_LOG = True

def log(*args, **kwargs):
    if DEBUG_LOG:
        print(*args, **kwargs)

class ImageKitStorage(Storage):
    def __init__(self):
        self.imagekit = ImageKit(
            private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
            public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
            url_endpoint=os.getenv("IMAGEKIT_URL_ENDPOINT"),
        )
        # fallback papka nisbiy MEDIA_ROOT ichida
        self.media_root = os.getenv("MEDIA_ROOT") or None
        self.media_url = os.getenv("MEDIA_URL", "/media/").rstrip("/") + "/"

    def _save(self, name, content):
        """
        content: fayl-like obyekt (InMemoryUploadedFile yoki TemporaryUploadedFile)
        name: modelda saqlanadigan nom (upload_to natijasi)
        """
        log(">>> ImageKitStorage._save called; name:", name, "content:", type(content))

        # 1) Agar content yo'q (None) => tahrir paytida fayl saqlanmaydi, shunchaki nomni qaytar
        if content is None:
            log("    content is None -> returning existing name:", name)
            return name or ""

        # 2) Fayl nomini aniqlash
        if not name:
            name = getattr(content, "name", "unnamed_file")
            log("    name was empty, using:", name)

        # 3) Faylni o'qish: ba'zida content.read() bo'sh yoki content yopilgan bo'lishi mumkin
        file_data = None
        try:
            # ba'zi obyektlarda read() masofali, qaytishi bytes
            file_data = content.read()
            log("    read() returned bytes length:", 0 if file_data is None else len(file_data))
            if not file_data:
                # urinib ko'ramiz: ochib o'qish
                try:
                    content.open()
                    file_data = content.read()
                    log("    after open() read length:", 0 if file_data is None else len(file_data))
                except Exception as e:
                    log("    Warning: couldn't open content:", e)
        except Exception as e:
            log("    Exception during content.read():", e)
            # har qanday holatda fallbackga o'tamiz pastda

        # 4) Agar file_data mavjud bo'lsa — ImageKit ga tashlaymiz
        if file_data:
            try:
                upload = self.imagekit.upload_file(
                    file=BytesIO(file_data),
                    file_name=name,
                )
                uploaded_name = getattr(upload, "name", None) or name
                log("    Uploaded to ImageKit, name:", uploaded_name, "url:", getattr(upload, "url", None))
                return uploaded_name
            except Exception as e:
                log("    ImageKit upload failed:", e)

        # 5) Agar ImageKit ishlamasa yoki file_data yo'q bo'lsa -> localga fallback yozamiz
        try:
            fallback_root = self.media_root or os.path.join(os.getcwd(), "media")
            fallback_dir = os.path.join(fallback_root, os.path.dirname(name))
            os.makedirs(fallback_dir, exist_ok=True)
            fallback_path = os.path.join(fallback_root, name)
            # agar file_data bo'lsa yozamiz, aks holda content ga qaytadan urinamiz
            if file_data:
                with open(fallback_path, "wb") as f:
                    f.write(file_data)
                log("    Fallback: wrote bytes to", fallback_path)
            else:
                # agar content obyektidan yana sinab o'qish mumkin bo'lsa
                try:
                    content.open()
                    with open(fallback_path, "wb") as f:
                        f.write(content.read())
                    log("    Fallback: wrote from content.open() to", fallback_path)
                except Exception as e:
                    # oxirgi chora: agar content hech narsa bermasa, yaratilgan nomni qaytamiz
                    log("    Fallback failed to read content:", e)
                    return name
            # DBda saqlanadigan nom — fallback uchun path nisbiy MEDIA_ROOT ga nisbatan
            relname = name
            log("    Returning fallback relname:", relname)
            return relname
        except Exception as e:
            log("    Final fallback exception:", e)
            # hech bo'lmasa nomni qaytamiz
            return name

    def url(self, name):
        # Agar name bo'sh => ''
        if not name:
            return ""
        # Agar name allaqachon to'liq URL bo'lsa => return
        if name.startswith("http://") or name.startswith("https://"):
            return name
        # Agar ImageKit endpoint bilan boshlangan bo'lsa, to'liq URL hosil qilamiz
        endpoint = os.getenv("IMAGEKIT_URL_ENDPOINT") or os.getenv("IMAGEKIT_URL_ENDPOINT".lower()) or ""
        if endpoint:
            endpoint = endpoint.rstrip("/")
            return f"{endpoint}/{name.lstrip('/')}"
        # Aks holda, fallback MEDIA_URL
        return f"{self.media_url}{name.lstrip('/')}"

    def exists(self, name):
        # Har doim False qaytarib, Django faylni qayta yozmasin
        return False
