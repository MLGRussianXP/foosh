# Generated by Django 4.2.9 on 2024-04-22 17:21

import catalog.models
from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0006_alter_item_school"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="image",
            field=sorl.thumbnail.fields.ImageField(
                upload_to=catalog.models.generate_image_filename,
                verbose_name="изображение",
            ),
        ),
    ]
