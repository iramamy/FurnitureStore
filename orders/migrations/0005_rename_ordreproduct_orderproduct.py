# Generated by Django 5.0.3 on 2024-05-18 15:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0004_alter_order_payment_alter_order_user"),
        ("shop", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="OrdreProduct",
            new_name="OrderProduct",
        ),
    ]
