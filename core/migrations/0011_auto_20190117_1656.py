# Generated by Django 2.1.5 on 2019-01-17 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_item_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lastlocation',
            name='survivor',
        ),
        migrations.AddField(
            model_name='survivor',
            name='latitude',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survivor',
            name='longitude',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='LastLocation',
        ),
    ]
