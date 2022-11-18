# Generated by Django 4.0.6 on 2022-11-05 19:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Недопустимый символ в username.', regex='^[\\w.@+-]')]),
        ),
    ]