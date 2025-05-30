# Generated by Django 5.1.6 on 2025-04-14 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_product', '0015_alter_ordercheckout_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercheckout',
            name='order_stats',
            field=models.CharField(choices=[('o0', 'قيد الانتظار'), ('o1', 'جار المعالجة'), ('o2', 'تم الشحن'), ('o3', 'تم التسليم'), ('o4', 'تم الإلغاء')], default='o0', max_length=2),
        ),
        migrations.AlterField(
            model_name='ordercheckout',
            name='payment_stats',
            field=models.CharField(choices=[('p0', 'لم يتم التسليم'), ('p1', 'تم التسليم')], default='p0', max_length=2),
        ),
    ]
