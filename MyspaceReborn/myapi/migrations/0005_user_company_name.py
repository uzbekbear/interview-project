# Generated by Django 3.1.2 on 2020-11-01 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0004_auto_20201101_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company_name',
            field=models.CharField(default=None, max_length=60, null=True),
        ),
    ]
