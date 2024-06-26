# Generated by Django 4.2.9 on 2024-04-18 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        ("users", "0006_student_city"),
    ]

    operations = [
        migrations.AlterField(
            model_name="school",
            name="city",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cities_light.city",
                verbose_name="город",
            ),
        ),
        migrations.AlterField(
            model_name="school",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="city",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cities_light.city",
                verbose_name="город",
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
    ]
