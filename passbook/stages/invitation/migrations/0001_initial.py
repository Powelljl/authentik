# Generated by Django 3.0.5 on 2020-05-11 19:09

import uuid

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("passbook_flows", "0004_auto_20200510_2310"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="InvitationStage",
            fields=[
                (
                    "stage_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="passbook_flows.Stage",
                    ),
                ),
            ],
            options={
                "verbose_name": "Invitation Stage",
                "verbose_name_plural": "Invitation Stages",
            },
            bases=("passbook_flows.stage",),
        ),
        migrations.CreateModel(
            name="Invitation",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("expires", models.DateTimeField(blank=True, default=None, null=True)),
                (
                    "fixed_data",
                    django.contrib.postgres.fields.jsonb.JSONField(default=dict),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Invitation",
                "verbose_name_plural": "Invitations",
            },
        ),
    ]