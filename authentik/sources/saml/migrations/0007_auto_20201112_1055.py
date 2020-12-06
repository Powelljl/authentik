# Generated by Django 3.1.3 on 2020-11-12 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_crypto", "0002_create_self_signed_kp"),
        ("authentik_sources_saml", "0006_samlsource_allow_idp_initiated"),
    ]

    operations = [
        migrations.AddField(
            model_name="samlsource",
            name="digest_algorithm",
            field=models.CharField(
                choices=[("sha1", "SHA1"), ("sha256", "SHA256")],
                default="sha256",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="samlsource",
            name="signature_algorithm",
            field=models.CharField(
                choices=[
                    ("rsa-sha1", "RSA-SHA1"),
                    ("rsa-sha256", "RSA-SHA256"),
                    ("ecdsa-sha256", "ECDSA-SHA256"),
                    ("dsa-sha1", "DSA-SHA1"),
                ],
                default="rsa-sha256",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="samlsource",
            name="signing_kp",
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text="Keypair which is used to sign outgoing requests. Leave empty to disable signing.",
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="authentik_crypto.certificatekeypair",
                verbose_name="Singing Keypair",
            ),
        ),
    ]