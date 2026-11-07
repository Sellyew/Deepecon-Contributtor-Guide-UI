"""Settings for the DeepEcon contributor site (implementation plan v0.3, D-043).

One settings file for both stages; the stage is chosen with DEEPECON_STAGE.

* Stage 0 (default): the demo on a team member's computer. The site listens only on the
  loopback address and holds only synthetic and demo material (P-053, adopted in D-043).
* Stage 1: one project-controlled server, set up before the first outside contributor (M6).

All state lives in one data folder (DEEPECON_DATA_DIR): the SQLite database, private files,
and, at Stage 0, the generated secret key. Moving the site means installing the pinned
application with Stage 1 settings and, if wanted, copying that folder.

The site sends nothing to AI services and loads no third-party content (D-042).
"""
import os
import secrets
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent          # implementations/contributor-interface
REPO_ROOT = BASE_DIR.parent.parent
SCHEMA_DIR = REPO_ROOT / "schemas" / "contributor-interface"
VALIDATION_DIR = REPO_ROOT / "validation"

STAGE = os.environ.get("DEEPECON_STAGE", "0")
if STAGE not in ("0", "1"):
    raise ImproperlyConfigured("DEEPECON_STAGE must be 0 (demo computer) or 1 (server).")

DATA_DIR = Path(os.environ.get("DEEPECON_DATA_DIR", BASE_DIR / "data")).resolve()
PRIVATE_STORAGE_ROOT = DATA_DIR / "private"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def _secret_key():
    key = os.environ.get("DEEPECON_SECRET_KEY")
    if key:
        return key
    if STAGE != "0":
        raise ImproperlyConfigured("Set DEEPECON_SECRET_KEY at Stage 1.")
    path = DATA_DIR / "secret_key"
    if not path.exists():
        path.write_text(secrets.token_urlsafe(50), encoding="utf-8")
        path.chmod(0o600)
    return path.read_text(encoding="utf-8").strip()


SECRET_KEY = _secret_key()
DEBUG = STAGE == "0" and os.environ.get("DEEPECON_DEBUG", "1") == "1"

if STAGE == "0":
    ALLOWED_HOSTS = ["127.0.0.1", "localhost", "[::1]"]
else:
    ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DEEPECON_ALLOWED_HOSTS", "").split(",") if h.strip()]
    if not ALLOWED_HOSTS:
        raise ImproperlyConfigured("Set DEEPECON_ALLOWED_HOSTS at Stage 1.")

INSTALLED_APPS = [
    # The project's apps come first so that papers' runserver (loopback only at Stage 0)
    # overrides the staticfiles version.
    "papers",
    "contributors",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "deepecon_site.middleware.SecurityHeadersMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "deepecon_site.urls"
WSGI_APPLICATION = "deepecon_site.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATA_DIR / "db.sqlite3",
        "OPTIONS": {"init_command": "PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL"},
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Interface languages (D-030): one gettext catalogue per language. Item text is never
# translated; per-paper labels come from the paper configuration.
LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English"), ("zh-hans", "简体中文")]
LOCALE_PATHS = [BASE_DIR / "locale"]
USE_I18N = True
TIME_ZONE = "UTC"
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = DATA_DIR / "static"

# Sessions and cookies.
SESSION_COOKIE_AGE = 14 * 24 * 3600
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = LANGUAGE_COOKIE_SECURE = STAGE == "1"
LANGUAGE_COOKIE_HTTPONLY = True
LANGUAGE_COOKIE_SAMESITE = "Lax"

# Security headers. The Content-Security-Policy is added by SecurityHeadersMiddleware.
SECURE_CONTENT_TYPE_NOSNIFF = True
# same-origin: browsers send no Referer to other sites. ("no-referrer" would make browsers send
# "Origin: null" on form posts, which fails Django's CSRF check.) Invitation-link URLs get
# "no-referrer" from SecurityHeadersMiddleware, so a token never travels in a Referer header.
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
if STAGE == "1":
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31536000

# Invitations (D-043, plan §2.2).
INVITATION_DAYS = int(os.environ.get("DEEPECON_INVITATION_DAYS", "30"))
SITE_BASE_URL = os.environ.get("DEEPECON_SITE_BASE_URL", "http://127.0.0.1:8000")

# Version of the notice text that contributors acknowledge (MVP §3 step 1; D-042).
NOTICE_VERSION = "2026-11-07"

# Request logs record paths with invitation tokens removed (plan §3).
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"redact_tokens": {"()": "deepecon_site.logging_filters.RedactInvitationTokens"}},
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django.server": {"handlers": ["console"], "level": "INFO", "filters": ["redact_tokens"], "propagate": False},
        "django.request": {"handlers": ["console"], "level": "WARNING", "filters": ["redact_tokens"], "propagate": False},
    },
}
