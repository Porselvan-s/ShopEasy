# Generated by Django 4.2.7 on 2024-01-01 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_favourite'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product',
            new_name='product_id',
        ),
    ]
