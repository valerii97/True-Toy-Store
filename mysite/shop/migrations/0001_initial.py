# Generated by Django 3.2.8 on 2021-10-24 14:25

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('phone', models.CharField(max_length=30)),
                ('is_registered', models.BooleanField(default=False)),
                ('address', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 10, 24, 14, 25, 18, 362660, tzinfo=utc))),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(max_length=30)),
                ('sum', models.FloatField()),
                ('status', models.CharField(choices=[('NEW', 'New'), ('COM', 'Completed'), ('CAN', 'Canceled')], default='NEW', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('price', models.FloatField()),
                ('Quantity in stock', models.IntegerField(default=0)),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='shop/images/')),
                ('category', models.ManyToManyField(default='df', to='shop.Category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255, null=True)),
                ('price', models.FloatField(default=None, null=True)),
                ('quantity', models.IntegerField(default=None, null=True)),
                ('sum', models.FloatField(default=None, null=True)),
                ('order_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_post_office', models.BooleanField(verbose_name='???? ??????????????????')),
                ('by_courier', models.BooleanField(verbose_name='????????????????')),
                ('delivery_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.deliveryservice')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255, null=True)),
                ('house', models.CharField(max_length=255, null=True)),
                ('appartment', models.CharField(max_length=255, null=True)),
                ('post_office', models.CharField(max_length=255, null=True)),
                ('order_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
            ],
        ),
    ]
