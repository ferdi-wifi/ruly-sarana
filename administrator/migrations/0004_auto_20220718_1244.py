# Generated by Django 3.1.7 on 2022-07-18 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_auto_20220717_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temppenyewa',
            name='id_transaksi',
        ),
        migrations.AddField(
            model_name='temppenyewa',
            name='petugas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administrator.petugas'),
        ),
    ]
