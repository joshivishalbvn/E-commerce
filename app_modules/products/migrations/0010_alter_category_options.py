# Generated by Django 5.1.1 on 2024-12-16 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_products_products_pr_vendor__90421d_idx'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-created_at'], 'verbose_name': 'Course Category', 'verbose_name_plural': 'Course Categories'},
        ),
    ]
