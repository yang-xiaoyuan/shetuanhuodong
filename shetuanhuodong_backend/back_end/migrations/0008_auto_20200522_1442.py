# Generated by Django 3.0.4 on 2020-05-22 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_end', '0007_auto_20200518_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nickname',
            name='nick_name',
            field=models.CharField(max_length=10),
        ),
    ]