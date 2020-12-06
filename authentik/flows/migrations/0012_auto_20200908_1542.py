# Generated by Django 3.1.1 on 2020-09-08 15:42

import django.db.models.deletion
from django.db import migrations, models

import authentik.lib.models


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_flows", "0011_flow_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flowstagebinding",
            name="stage",
            field=authentik.lib.models.InheritanceForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="authentik_flows.stage"
            ),
        ),
        migrations.AlterField(
            model_name="stage",
            name="name",
            field=models.TextField(unique=True),
        ),
    ]