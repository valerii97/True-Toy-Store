# Generated by Django 3.2.8 on 2021-10-25 22:49

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20211026_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 25, 22, 49, 6, 605055, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_method', models.CharField(max_length=100)),
                ('order_num', models.ForeignKey(default='df', on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
            ],
        ),
    ]
