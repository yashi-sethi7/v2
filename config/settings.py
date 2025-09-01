import os
from dotenv import load_dotenv

load_dotenv()

# App Configuration
APP_TITLE = os.getenv('APP_TITLE', 'My Digital Lookbook')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/images/uploads')

# Page Configuration
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": "👔",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Image Upload Settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp']

# UI Constants
CATEGORIES_PER_ROW = 4
ITEMS_PER_PAGE = 12
DEFAULT_IMAGE_SIZE = (300, 400)
