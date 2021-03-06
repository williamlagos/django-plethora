# Generated by Django 3.0.5 on 2020-04-24 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plethora', '0002_image_playable_product_spreadable_spreadbasket_spreaded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='description',
            field=models.CharField(default='', max_length=140),
        ),
        migrations.AlterField(
            model_name='image',
            name='link',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(default='!%', max_length=10),
        ),
        migrations.AlterField(
            model_name='playable',
            name='name',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='playable',
            name='visual',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='spreadable',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='spreadable',
            name='spreaded',
            field=models.CharField(default='efforia', max_length=15),
        ),
        migrations.AlterField(
            model_name='spreaded',
            name='name',
            field=models.CharField(default='!!', max_length=10),
        ),
        migrations.DeleteModel(
            name='SpreadBasket',
        ),
    ]
