# Generated by Django 4.2.9 on 2024-04-23 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment",
            field=models.CharField(
                default="", max_length=255, verbose_name="платеж"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="итого",
            ),
        ),
    ]
