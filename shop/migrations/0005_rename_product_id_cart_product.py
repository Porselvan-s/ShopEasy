# Generated by Django 4.2.7 on 2024-01-01 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_rename_product_cart_product_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product_id',
            new_name='product',
        ),
    ]
