# Generated by Django 3.0.4 on 2020-11-01 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appFactInv', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productos',
            options={'ordering': ['id'], 'verbose_name': 'producto', 'verbose_name_plural': 'productos'},
        ),
    ]
