# Generated by Django 2.1.5 on 2019-01-18 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20190117_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survivor',
            name='flag_survivor',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
