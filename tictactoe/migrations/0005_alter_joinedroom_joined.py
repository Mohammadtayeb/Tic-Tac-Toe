# Generated by Django 3.2.2 on 2023-03-21 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictactoe', '0004_joinedroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinedroom',
            name='joined',
            field=models.CharField(max_length=64),
        ),
    ]