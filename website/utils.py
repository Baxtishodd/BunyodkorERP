# Example: in any app
# from .utils import get_random_color

# Example: Importing from project root folder
# from my_project_name.utils import get_random_color

# Example: Importing from a specific app's utils.py
# from my_app.utils import get_random_color

import random

def get_random_color():
    """Generates a random color in HEX format."""
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))