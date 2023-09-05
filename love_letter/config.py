import os

REPOSITORY_IMPL = os.environ.get("repository_impl")
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", 27017)
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME", "love_letter")
DB_COLLECTION = os.environ.get("DB_COLLECTION", "love_letter")
FRONTEND_HOST = os.environ.get("FRONTEND_HOST", "http://127.0.0.1")
