# Generated by Django 5.1.1 on 2024-09-22 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_address_street'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.TextField(default='UNKNOWN', max_length=30),
        ),
    ]
