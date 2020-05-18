# Generated by Django 3.0.5 on 2020-05-10 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("passbook_stages_identification", "0003_auto_20200509_2025"),
    ]

    operations = [
        migrations.AlterField(
            model_name="identificationstage",
            name="template",
            field=models.TextField(
                choices=[
                    ("stages/identification/login.html", "Default Login"),
                    ("stages/identification/recovery.html", "Default Recovery"),
                ]
            ),
        ),
    ]