# Generated by Django 4.2.1 on 2023-07-06 17:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0016_ingredientrecipe_unique_ingredient_in_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='quantity',
            field=models.PositiveSmallIntegerField(
                help_text='Содержит количество ингридиента',
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(32767),
                ],
                verbose_name='Количество ингридиента',
            ),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(
                help_text='Содержит время приготовления рецепта',
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(32767),
                ],
                verbose_name='Время приготовления',
            ),
        ),
    ]
