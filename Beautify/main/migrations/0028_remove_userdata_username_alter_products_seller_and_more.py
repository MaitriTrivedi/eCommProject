# Generated by Django 4.2.4 on 2023-08-18 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('main', '0027_userdata_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='username',
        ),
        migrations.AlterField(
            model_name='products',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.sellers'),
        ),
        migrations.DeleteModel(
            name='Sellers',
        ),
        migrations.DeleteModel(
            name='UserData',
        ),
    ]
