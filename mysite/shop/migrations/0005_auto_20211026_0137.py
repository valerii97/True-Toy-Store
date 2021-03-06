# Generated by Django 3.2.8 on 2021-10-25 22:37

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20211025_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryservice',
            name='slug',
            field=models.SlugField(max_length=40),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 25, 22, 36, 33, 367779, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='sum',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='shop.Category'),
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('order_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
            ],
        ),
    ]
