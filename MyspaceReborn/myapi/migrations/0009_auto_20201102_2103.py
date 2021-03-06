# Generated by Django 3.1.3 on 2020-11-02 19:03

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0008_auto_20201101_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='liked_posts',
            field=models.CharField(blank=True, default='', max_length=600, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
        migrations.AddField(
            model_name='user',
            name='num_posts_published',
            field=models.IntegerField(default=0),
        ),
    ]
