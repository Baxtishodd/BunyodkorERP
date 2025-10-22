import sys
import os

# Bu faylning joriy katalogini aniqlash
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# dcrm joylashgan joyni sys.path ga qo‘shish
sys.path.insert(0, BASE_DIR)

from dcrm.wsgi import application
