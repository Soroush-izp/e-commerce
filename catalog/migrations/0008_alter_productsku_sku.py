# Generated by Django 5.1.1 on 2024-10-25 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_productdetail_order_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsku',
            name='sku',
            field=models.CharField(editable=False, max_length=100, unique=True),
        ),
    ]