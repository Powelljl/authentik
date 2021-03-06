# Generated by Django 3.0.6 on 2020-05-19 22:08

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "event_uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "action",
                    models.TextField(
                        choices=[
                            ("LOGIN", "login"),
                            ("LOGIN_FAILED", "login_failed"),
                            ("LOGOUT", "logout"),
                            ("AUTHORIZE_APPLICATION", "authorize_application"),
                            ("SUSPICIOUS_REQUEST", "suspicious_request"),
                            ("SIGN_UP", "sign_up"),
                            ("PASSWORD_RESET", "password_reset"),
                            ("INVITE_CREATED", "invitation_created"),
                            ("INVITE_USED", "invitation_used"),
                            ("CUSTOM", "custom"),
                        ]
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("app", models.TextField()),
                (
                    "context",
                    models.JSONField(blank=True, default=dict),
                ),
                ("client_ip", models.GenericIPAddressField(null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
            },
        ),
    ]
