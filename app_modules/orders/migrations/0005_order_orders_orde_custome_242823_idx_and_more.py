# Generated by Django 5.1.1 on 2024-10-18 06:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_options_alter_orderitem_options_payment'),
        ('products', '0008_stockhistory_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['customer', 'created_at'], name='orders_orde_custome_242823_idx'),
        ),
        migrations.AddIndex(
            model_name='orderitem',
            index=models.Index(fields=['order', 'product'], name='orders_orde_order_i_52f79a_idx'),
        ),
    ]