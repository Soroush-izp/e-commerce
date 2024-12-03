# Generated by Django 5.1.1 on 2024-11-18 10:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_address_phone_number_address_title'),
        ('orders', '0005_orderdetails_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.address'),
        ),
    ]
