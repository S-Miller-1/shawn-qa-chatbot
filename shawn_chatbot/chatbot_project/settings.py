"""Minimal Django settings for the terminal chatbot."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "local-terminal-chatbot-only"
DEBUG = False

INSTALLED_APPS = ["chat"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "django.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"