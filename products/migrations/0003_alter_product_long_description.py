# Generated by Django 4.1.7 on 2023-04-04 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_has_review_product_review_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='long_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]