# Generated by Django 5.1.6 on 2025-03-20 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'فئة', 'verbose_name_plural': 'الفئات'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'منتج', 'verbose_name_plural': 'المنتجات'},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'verbose_name': 'صورة منتج', 'verbose_name_plural': 'صور المنتجات'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'فئة فرعية', 'verbose_name_plural': 'الفئات الفرعية'},
        ),
        migrations.AddField(
            model_name='product',
            name='product_color',
            field=models.CharField(choices=[('a', 'أحمر'), ('b', 'أزرق'), ('c', 'أصفر'), ('d', 'أخضر'), ('e', 'برتقالي'), ('f', 'بنفسجي'), ('g', 'أسود'), ('h', 'أبيض'), ('i', 'رمادي'), ('j', 'بني'), ('k', 'وردي'), ('l', 'بيج')], default='h', max_length=10, verbose_name='اللون'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_age_range',
            field=models.CharField(choices=[('a', '1-3 أشهر'), ('b', '3-4 أشهر'), ('c', '4-6 أشهر'), ('d', '6-9 أشهر'), ('e', '9-12 أشهر'), ('f', 'سنة'), ('g', 'لكل الأعمار')], default='g', max_length=50, verbose_name='الفئة العمرية'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_gender',
            field=models.CharField(choices=[('a', 'ذكر'), ('b', 'أنثى'), ('c', 'للجنسين')], default='c', max_length=10, verbose_name='الجنس'),
        ),
    ]
