# Generated by Django 4.0.6 on 2022-11-01 09:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0003_ingredientinrecipe'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientinrecipe',
            options={'verbose_name': 'Amount ingredients in recipe', 'verbose_name_plural': 'Amount ingredients in recipes'},
        ),
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.ingredient', verbose_name='Ingredient'),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, help_text='Add image', null=True, upload_to='recipe/', verbose_name='Image')),
                ('text', models.TextField(help_text='Add text', verbose_name='Text')),
                ('cooking_time', models.PositiveSmallIntegerField(verbose_name='Cooking time')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('ingredients', models.ManyToManyField(to='recipe.ingredientinrecipe', verbose_name='Necessary ingredients')),
                ('tags', models.ManyToManyField(to='recipe.tag')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
            },
        ),
    ]