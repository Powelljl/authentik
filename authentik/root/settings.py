"""
Django settings for authentik project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import importlib
import logging
import os
import sys
from json import dumps
from time import time

import structlog
from celery.schedules import crontab
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from authentik import __version__
from authentik.core.middleware import structlog_add_request_id
from authentik.lib.config import CONFIG
from authentik.lib.logging import add_process_id
from authentik.lib.sentry import before_send


def j_print(event: str, log_level: str = "info", **kwargs):
    """Print event in the same format as structlog with JSON.
    Used before structlog is configured."""
    data = {
        "event": event,
        "level": log_level,
        "logger": __name__,
        "timestamp": time(),
    }
    data.update(**kwargs)
    print(dumps(data), file=sys.stderr)


LOGGER = structlog.get_logger()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_ROOT = BASE_DIR + "/static"
STATICFILES_DIRS = [BASE_DIR + "/web"]
MEDIA_ROOT = BASE_DIR + "/media"

SECRET_KEY = CONFIG.y(
    "secret_key", "9$@r!d^1^jrn#fk#1#@ks#9&i$^s#1)_13%$rwjrhd=e8jfi_s"
)  # noqa Debug

DEBUG = CONFIG.y_bool("debug")
INTERNAL_IPS = ["127.0.0.1"]
ALLOWED_HOSTS = ["*"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LOGIN_URL = "authentik_flows:default-authentication"

# Custom user model
AUTH_USER_MODEL = "authentik_core.User"

_cookie_suffix = "_debug" if DEBUG else ""
CSRF_COOKIE_NAME = "authentik_csrf"
LANGUAGE_COOKIE_NAME = f"authentik_language{_cookie_suffix}"
SESSION_COOKIE_NAME = f"authentik_session{_cookie_suffix}"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "authentik.admin.apps.AuthentikAdminConfig",
    "authentik.api.apps.AuthentikAPIConfig",
    "authentik.events.apps.AuthentikEventsConfig",
    "authentik.crypto.apps.AuthentikCryptoConfig",
    "authentik.flows.apps.AuthentikFlowsConfig",
    "authentik.outposts.apps.AuthentikOutpostConfig",
    "authentik.lib.apps.AuthentikLibConfig",
    "authentik.policies.apps.AuthentikPoliciesConfig",
    "authentik.policies.dummy.apps.AuthentikPolicyDummyConfig",
    "authentik.policies.event_matcher.apps.AuthentikPoliciesEventMatcherConfig",
    "authentik.policies.expiry.apps.AuthentikPolicyExpiryConfig",
    "authentik.policies.expression.apps.AuthentikPolicyExpressionConfig",
    "authentik.policies.group_membership.apps.AuthentikPoliciesGroupMembershipConfig",
    "authentik.policies.hibp.apps.AuthentikPolicyHIBPConfig",
    "authentik.policies.password.apps.AuthentikPoliciesPasswordConfig",
    "authentik.policies.reputation.apps.AuthentikPolicyReputationConfig",
    "authentik.providers.proxy.apps.AuthentikProviderProxyConfig",
    "authentik.providers.oauth2.apps.AuthentikProviderOAuth2Config",
    "authentik.providers.saml.apps.AuthentikProviderSAMLConfig",
    "authentik.recovery.apps.AuthentikRecoveryConfig",
    "authentik.sources.ldap.apps.AuthentikSourceLDAPConfig",
    "authentik.sources.oauth.apps.AuthentikSourceOAuthConfig",
    "authentik.sources.saml.apps.AuthentikSourceSAMLConfig",
    "authentik.stages.captcha.apps.AuthentikStageCaptchaConfig",
    "authentik.stages.consent.apps.AuthentikStageConsentConfig",
    "authentik.stages.dummy.apps.AuthentikStageDummyConfig",
    "authentik.stages.email.apps.AuthentikStageEmailConfig",
    "authentik.stages.prompt.apps.AuthentikStagPromptConfig",
    "authentik.stages.identification.apps.AuthentikStageIdentificationConfig",
    "authentik.stages.invitation.apps.AuthentikStageUserInvitationConfig",
    "authentik.stages.user_delete.apps.AuthentikStageUserDeleteConfig",
    "authentik.stages.user_login.apps.AuthentikStageUserLoginConfig",
    "authentik.stages.user_logout.apps.AuthentikStageUserLogoutConfig",
    "authentik.stages.user_write.apps.AuthentikStageUserWriteConfig",
    "authentik.stages.authenticator_static.apps.AuthentikStageAuthenticatorStaticConfig",
    "authentik.stages.authenticator_totp.apps.AuthentikStageAuthenticatorTOTPConfig",
    "authentik.stages.authenticator_validate.apps.AuthentikStageAuthenticatorValidateConfig",
    "authentik.stages.authenticator_webauthn.apps.AuthentikStageAuthenticatorWebAuthnConfig",
    "authentik.stages.password.apps.AuthentikStagePasswordConfig",
    "rest_framework",
    "django_filters",
    "drf_yasg2",
    "guardian",
    "django_prometheus",
    "channels",
    "dbbackup",
    "authentik.managed.apps.AuthentikManagedConfig",
]

GUARDIAN_MONKEY_PATCH = False

SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "authentik.api.v2.urls.info",
    "SECURITY_DEFINITIONS": {
        "token": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "authentik.api.pagination.Pagination",
    "PAGE_SIZE": 100,
    "DATETIME_FORMAT": "%s",
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework_guardian.filters.ObjectPermissionsFilter",
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.DjangoObjectPermissions",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "authentik.api.auth.AuthentikTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": (
            f"redis://:{CONFIG.y('redis.password')}@{CONFIG.y('redis.host')}:6379"
            f"/{CONFIG.y('redis.cache_db')}"
        ),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_SAMESITE = "lax"

MESSAGE_STORAGE = "authentik.root.messages.storage.ChannelsStorage"

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "authentik.core.middleware.RequestIDMiddleware",
    "authentik.events.middleware.AuditMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "authentik.core.middleware.ImpersonateMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "authentik.root.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "authentik.lib.config.context_processor",
            ],
        },
    },
]

ASGI_APPLICATION = "authentik.root.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                f"redis://:{CONFIG.y('redis.password')}@{CONFIG.y('redis.host')}:6379"
                f"/{CONFIG.y('redis.ws_db')}"
            ],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": CONFIG.y("postgresql.host"),
        "NAME": CONFIG.y("postgresql.name"),
        "USER": CONFIG.y("postgresql.user"),
        "PASSWORD": CONFIG.y("postgresql.password"),
    }
}

# Email
EMAIL_HOST = CONFIG.y("email.host")
EMAIL_PORT = int(CONFIG.y("email.port"))
EMAIL_HOST_USER = CONFIG.y("email.username")
EMAIL_HOST_PASSWORD = CONFIG.y("email.password")
EMAIL_USE_TLS = CONFIG.y("email.use_tls")
EMAIL_USE_SSL = CONFIG.y("email.use_ssl")
EMAIL_TIMEOUT = int(CONFIG.y("email.timeout"))
DEFAULT_FROM_EMAIL = CONFIG.y("email.from")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = "[authentik] "

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Celery settings
# Add a 10 minute timeout to all Celery tasks.
CELERY_TASK_SOFT_TIME_LIMIT = 600
CELERY_BEAT_SCHEDULE = {
    "clean_expired_models": {
        "task": "authentik.core.tasks.clean_expired_models",
        "schedule": crontab(minute="*/5"),
        "options": {"queue": "authentik_scheduled"},
    },
    "db_backup": {
        "task": "authentik.core.tasks.backup_database",
        "schedule": crontab(minute=0, hour=0),
        "options": {"queue": "authentik_scheduled"},
    },
}
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_TASK_DEFAULT_QUEUE = "authentik"
CELERY_BROKER_URL = (
    f"redis://:{CONFIG.y('redis.password')}@{CONFIG.y('redis.host')}"
    f":6379/{CONFIG.y('redis.message_queue_db')}"
)
CELERY_RESULT_BACKEND = (
    f"redis://:{CONFIG.y('redis.password')}@{CONFIG.y('redis.host')}"
    f":6379/{CONFIG.y('redis.message_queue_db')}"
)

# Database backup
DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "./backups" if DEBUG else "/backups"}
DBBACKUP_CONNECTOR_MAPPING = {
    "django_prometheus.db.backends.postgresql": "dbbackup.db.postgresql.PgDumpConnector"
}
if CONFIG.y("postgresql.s3_backup"):
    DBBACKUP_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    DBBACKUP_STORAGE_OPTIONS = {
        "access_key": CONFIG.y("postgresql.s3_backup.access_key"),
        "secret_key": CONFIG.y("postgresql.s3_backup.secret_key"),
        "bucket_name": CONFIG.y("postgresql.s3_backup.bucket"),
        "region_name": CONFIG.y("postgresql.s3_backup.region", "eu-central-1"),
        "default_acl": "private",
        "endpoint_url": CONFIG.y("postgresql.s3_backup.host"),
    }
    j_print(
        "Database backup to S3 is configured.",
        host=CONFIG.y("postgresql.s3_backup.host"),
    )

# Sentry integration
_ERROR_REPORTING = CONFIG.y_bool("error_reporting.enabled", False)
if not DEBUG and _ERROR_REPORTING:
    sentry_init(
        dsn="https://a579bb09306d4f8b8d8847c052d3a1d3@sentry.beryju.org/8",
        integrations=[
            DjangoIntegration(transaction_style="function_name"),
            CeleryIntegration(),
            RedisIntegration(),
        ],
        before_send=before_send,
        release=f"authentik@{__version__}",
        traces_sample_rate=0.6,
        environment=CONFIG.y("error_reporting.environment", "customer"),
        send_default_pii=CONFIG.y_bool("error_reporting.send_pii", False),
    )
    j_print(
        "Error reporting is enabled.",
        env=CONFIG.y("error_reporting.environment", "customer"),
    )


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

LOG_LEVEL = CONFIG.y("log_level").upper()


structlog.configure_once(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.threadlocal.merge_threadlocal_context,
        add_process_id,
        structlog_add_request_id,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=False),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(
        getattr(logging, LOG_LEVEL, logging.WARNING)
    ),
    cache_logger_on_first_use=True,
)

LOG_PRE_CHAIN = [
    # Add the log level and a timestamp to the event_dict if the log entry
    # is not from structlog.
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    structlog.processors.TimeStamper(),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(sort_keys=True),
            "foreign_pre_chain": LOG_PRE_CHAIN,
        },
        "colored": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=DEBUG),
            "foreign_pre_chain": LOG_PRE_CHAIN,
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "colored" if DEBUG else "plain",
        },
    },
    "loggers": {},
}

TEST = False
TEST_RUNNER = "authentik.root.test_runner.PytestTestRunner"

_LOGGING_HANDLER_MAP = {
    "": LOG_LEVEL,
    "authentik": LOG_LEVEL,
    "django": "WARNING",
    "celery": "WARNING",
    "selenium": "WARNING",
    "grpc": LOG_LEVEL,
    "docker": "WARNING",
    "urllib3": "WARNING",
    "websockets": "WARNING",
    "daphne": "WARNING",
    "dbbackup": "ERROR",
    "kubernetes": "INFO",
    "asyncio": "WARNING",
    "aioredis": "WARNING",
}
for handler_name, level in _LOGGING_HANDLER_MAP.items():
    # pyright: reportGeneralTypeIssues=false
    LOGGING["loggers"][handler_name] = {
        "handlers": ["console"],
        "level": level,
        "propagate": False,
    }


_DISALLOWED_ITEMS = [
    "INSTALLED_APPS",
    "MIDDLEWARE",
    "AUTHENTICATION_BACKENDS",
    "CELERY_BEAT_SCHEDULE",
]
# Load subapps's INSTALLED_APPS
for _app in INSTALLED_APPS:
    if _app.startswith("authentik"):
        if "apps" in _app:
            _app = ".".join(_app.split(".")[:-2])
        try:
            app_settings = importlib.import_module("%s.settings" % _app)
            INSTALLED_APPS.extend(getattr(app_settings, "INSTALLED_APPS", []))
            MIDDLEWARE.extend(getattr(app_settings, "MIDDLEWARE", []))
            AUTHENTICATION_BACKENDS.extend(
                getattr(app_settings, "AUTHENTICATION_BACKENDS", [])
            )
            CELERY_BEAT_SCHEDULE.update(
                getattr(app_settings, "CELERY_BEAT_SCHEDULE", {})
            )
            for _attr in dir(app_settings):
                if not _attr.startswith("__") and _attr not in _DISALLOWED_ITEMS:
                    globals()[_attr] = getattr(app_settings, _attr)
        except ImportError:
            pass

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    CELERY_TASK_ALWAYS_EAGER = True

INSTALLED_APPS.append("authentik.core.apps.AuthentikCoreConfig")

j_print("Booting authentik", version=__version__)
