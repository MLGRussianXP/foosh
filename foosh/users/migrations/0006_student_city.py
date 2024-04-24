# Generated by Django 4.2.9 on 2024-04-13 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        ("users", "0005_alter_school_city"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="city",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cities_light.city",
            ),
        ),
    ]
