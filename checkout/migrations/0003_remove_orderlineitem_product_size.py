# Generated by Django 4.1.7 on 2023-04-19 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_rename_original_bag_order_original_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlineitem',
            name='product_size',
        ),
    ]