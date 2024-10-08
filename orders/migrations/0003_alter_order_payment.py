# Generated by Django 5.0.3 on 2024-05-18 12:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_remove_order_country_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="orders.payment",
            ),
        ),
    ]
