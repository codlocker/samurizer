# Generated by Django 2.0.1 on 2018-02-15 15:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('samuri', '0003_auto_20180215_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newscontent',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 15, 15, 57, 1, 884152, tzinfo=utc)),
        ),
    ]
