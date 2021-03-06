# Generated by Django 3.0.6 on 2020-05-24 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_sources_ldap", "0003_default_ldap_property_mappings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ldapsource",
            name="additional_group_dn",
            field=models.TextField(
                blank=True,
                help_text="Prepended to Base DN for Group-queries.",
                verbose_name="Addition Group DN",
            ),
        ),
        migrations.AlterField(
            model_name="ldapsource",
            name="additional_user_dn",
            field=models.TextField(
                blank=True,
                help_text="Prepended to Base DN for User-queries.",
                verbose_name="Addition User DN",
            ),
        ),
    ]
