# Generated by Django 5.1.6 on 2025-03-23 03:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_product', '0007_alter_cart_options_alter_cartitem_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='_product.cart', verbose_name='السلة'),
        ),
    ]
