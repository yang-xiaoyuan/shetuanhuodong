# Generated by Django 3.0.4 on 2020-05-18 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_end', '0006_auto_20200505_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]