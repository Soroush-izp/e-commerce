# Generated by Django 5.1.1 on 2024-11-25 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_orderdetails_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shopingcart',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
