# Generated by Django 3.0.6 on 2020-05-23 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_flows", "0003_auto_20200523_1133"),
        ("authentik_core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="application",
            name="skip_authorization",
        ),
        migrations.AddField(
            model_name="source",
            name="authentication_flow",
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text="Flow to use when authenticating existing users.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="source_authentication",
                to="authentik_flows.Flow",
            ),
        ),
        migrations.AddField(
            model_name="source",
            name="enrollment_flow",
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text="Flow to use when enrolling new users.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="source_enrollment",
                to="authentik_flows.Flow",
            ),
        ),
        migrations.AddField(
            model_name="provider",
            name="authorization_flow",
            field=models.ForeignKey(
                help_text="Flow used when authorizing this provider.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="provider_authorization",
                to="authentik_flows.Flow",
            ),
        ),
    ]
