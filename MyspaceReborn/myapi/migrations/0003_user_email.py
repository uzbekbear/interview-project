# Generated by Django 3.1.2 on 2020-10-31 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0002_auto_20201031_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default='email_placeholder', max_length=60),
            preserve_default=False,
        ),
    ]