# Generated by Django 5.1.1 on 2024-10-04 09:11

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('website', models.URLField()),
                ('instagram', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='brand/brand_icons/')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('attributes', models.ManyToManyField(related_name='groups', to='catalog.attributetype')),
            ],
        ),
        migrations.CreateModel(
            name='BrandPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt', models.TextField()),
                ('photo', models.ImageField(upload_to='brand/brand_photos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='catalog.brand')),
            ],
        ),
        migrations.CreateModel(
            name='BrandVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt', models.TextField()),
                ('video', models.FileField(upload_to='brand/brand_videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv'])])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='catalog.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('photo', models.ImageField(upload_to='category/category_photos/')),
                ('description', models.TextField()),
                ('level', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='catalog.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('summary', models.TextField()),
                ('cover', models.ImageField(upload_to='product/product_covers/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('attribute_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='catalog.attributegroup')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalog.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='catalog.attributetype')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('value', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='catalog.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt', models.TextField()),
                ('photo', models.ImageField(upload_to='product/product_photos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='catalog.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skus', to='catalog.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt', models.TextField()),
                ('video', models.FileField(upload_to='product/product_videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv'])])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='catalog.product')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='catalog.product')),
            ],
            options={
                'unique_together': {('product', 'order_num')},
            },
        ),
        migrations.CreateModel(
            name='ReviewPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='review_photos/')),
                ('position', models.CharField(choices=[('center-large', 'CenterLarge'), ('left-small', 'LeftSmall'), ('right-small', 'RightSmall')], default='center-large', max_length=20)),
                ('review_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='catalog.reviewsection')),
            ],
            options={
                'ordering': ['order_num'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReviewText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.PositiveIntegerField()),
                ('text', models.TextField()),
                ('review_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='texts', to='catalog.reviewsection')),
            ],
            options={
                'ordering': ['order_num'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReviewVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.PositiveIntegerField()),
                ('video', models.FileField(upload_to='review_videos/')),
                ('position', models.CharField(choices=[('center-large', 'CenterLarge'), ('left-small', 'LeftSmall'), ('right-small', 'RightSmall')], default='center-large', max_length=20)),
                ('review_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='catalog.reviewsection')),
            ],
            options={
                'ordering': ['order_num'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductSKUAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.productattributevalue')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku_attributes', to='catalog.productsku')),
            ],
            options={
                'unique_together': {('sku', 'attribute_value')},
            },
        ),
    ]
