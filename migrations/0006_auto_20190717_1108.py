# Generated by Django 2.2.3 on 2019-07-17 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppl_order_tracking', '0005_auto_20190624_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='items_ordered',
            field=models.IntegerField(default=0, help_text='Enter 0 for all standing orders', null=True),
        ),
    ]