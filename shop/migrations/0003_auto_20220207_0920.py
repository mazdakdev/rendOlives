# Generated by Django 3.2.3 on 2022-02-07 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20220206_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='off_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productsizes',
            name='off_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
