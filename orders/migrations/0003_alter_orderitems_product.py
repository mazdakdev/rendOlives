# Generated by Django 3.2.3 on 2022-02-05 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_productsizes_product'),
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop.productsizes'),
        ),
    ]