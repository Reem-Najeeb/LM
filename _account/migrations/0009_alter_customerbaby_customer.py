# Generated by Django 5.1.6 on 2025-03-15 23:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_account', '0008_alter_customerbaby_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerbaby',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='baby', to='_account.customer'),
        ),
    ]
