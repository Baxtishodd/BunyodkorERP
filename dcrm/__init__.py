from django.core.files import storage as django_storage
from dcrm.storages import SupabaseStorage

# default_storage obyektini to‘g‘ridan-to‘g‘ri almashtiramiz
django_storage.default_storage = SupabaseStorage()

