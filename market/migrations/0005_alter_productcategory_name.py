# Generated by Django 4.2.3 on 2023-07-26 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_alter_productimage_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
