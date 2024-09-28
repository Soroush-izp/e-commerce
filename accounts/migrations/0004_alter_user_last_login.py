# Generated by Django 5.1.1 on 2024-09-15 15:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='Last Login'),
            preserve_default=False,
        ),
    ]