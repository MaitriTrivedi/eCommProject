# Generated by Django 4.1.7 on 2023-03-20 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_cartitems_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='total_price',
            field=models.FloatField(default=1000),
            preserve_default=False,
        ),
    ]
