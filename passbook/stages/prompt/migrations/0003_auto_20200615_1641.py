# Generated by Django 3.0.7 on 2020-06-15 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("passbook_stages_prompt", "0002_auto_20200528_2059"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prompt",
            name="type",
            field=models.CharField(
                choices=[
                    ("text", "Text"),
                    ("username", "Username"),
                    ("e-mail", "Email"),
                    ("password", "Password"),
                    ("number", "Number"),
                    ("checkbox", "Checkbox"),
                    ("data", "Date"),
                    ("data-time", "Date Time"),
                    ("separator", "Separator"),
                    ("hidden", "Hidden"),
                    ("static", "Static"),
                ],
                max_length=100,
            ),
        ),
    ]