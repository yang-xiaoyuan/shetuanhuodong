# Generated by Django 3.0.4 on 2020-05-22 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_end', '0008_auto_20200522_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='to_add_friends',
            field=models.CharField(default='', max_length=100),
        ),
    ]