# Generated by Django 4.2.3 on 2023-07-26 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_rename_category_productcategory'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Image',
            new_name='ProductImage',
        ),
    ]
