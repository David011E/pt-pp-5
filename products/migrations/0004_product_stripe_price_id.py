# Generated by Django 3.2.25 on 2024-04-18 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stripe_price_id',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
