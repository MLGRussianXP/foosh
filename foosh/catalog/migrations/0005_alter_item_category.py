# Generated by Django 4.2.9 on 2024-04-18 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_alter_item_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.IntegerField(
                choices=[
                    (None, "..."),
                    (1, "Выпечка"),
                    (2, "Напитки"),
                    (3, "Горячее"),
                    (4, "Комбо"),
                ],
                verbose_name="категория",
            ),
        ),
    ]
