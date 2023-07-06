"""Describe models of a Recipe app."""
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from foodgram.settings import (MAXIMUM_COOKING_TIME, MAXIMUM_INGREDIENT_AMOUNT,
                               MINIMUM_COOKING_TIME, MINIMUM_INGREDIENT_AMOUNT)

User = get_user_model()


class Ingredient(models.Model):
    """Describe a model which stores information about ingredients."""

    name = models.CharField(
        verbose_name='Название ингридиента',
        help_text='Содержит название ингридиента (макс 150 символов)',
        max_length=150,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения ингридиента',
        help_text='Содержит единицы измерения ингридиента (макс 50 символов)',
        max_length=50,
    )

    class Meta:
        """Describe settings for the Ingredient model."""

        ordering = ('name', 'measurement_unit')
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        """Show a name of an ingredient."""
        return self.name


class Tag(models.Model):
    """Describe a model which stores tags for recipes."""

    name = models.CharField(
        verbose_name='Название тэга',
        help_text='Содержит название тэга (макс 150 символов)',
        unique=True,
        max_length=150,
    )
    color = models.CharField(
        verbose_name='Цвет тэга',
        help_text='Содержит цвет тэга в HEX формате',
        max_length=7,
        validators=(validators.RegexValidator(regex='^#[0-9a-fA-F]{6}$'),),
    )
    slug = models.SlugField(
        verbose_name='Тексты ссылки тэга',
        help_text='Содержит короткий текст для доступа к тэгу через url',
        unique=True,
        max_length=50,
    )

    class Meta:
        """Describe settings for the Tag model."""

        ordering = ('name',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        """Show a name of a tag."""
        return self.name


class Recipe(models.Model):
    """Describe a model which stores recipes."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        help_text='Содержит ссылку на автора рецепта',
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        help_text='Содержит название рецепта (макс 150 символов)',
        max_length=150,
    )
    image = models.ImageField(
        verbose_name='Фото рецепта',
        help_text='Содержит фото рецепта',
        upload_to='media/',
    )
    description = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Содержит описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        help_text='Содержит список ингридиентов',
        through='IngredientRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        help_text='Содержит список тэгов',
        through='TagRecipe',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Содержит время приготовления рецепта',
        validators=(
            validators.MinValueValidator(MINIMUM_COOKING_TIME),
            validators.MaxValueValidator(MAXIMUM_COOKING_TIME),
        ),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления рецепта',
        help_text='Содержит дату добавления рецепта',
    )

    class Meta:
        """Describe settings for the Recipe model."""

        ordering = ('-pub_date', 'name')
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        """Show a name of a tag."""
        return self.name


class IngredientRecipe(models.Model):
    """Describe a model which stores ingredient - recipe connection."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество ингридиента',
        help_text='Содержит количество ингридиента',
        validators=(
            validators.MinValueValidator(MINIMUM_INGREDIENT_AMOUNT),
            validators.MaxValueValidator(MAXIMUM_INGREDIENT_AMOUNT),
        ),
    )

    def __str__(self):
        """Show a ingredient - recipe chain."""
        return f'{self.ingredient} {self.recipe}'

    class Meta:
        """Describe settings for the IngredientRecipe model."""

        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name="unique_ingredient_in_recipe",
            ),
        )


class TagRecipe(models.Model):
    """Describe a model which stores tag - recipe connection."""

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """Show a tag - recipe chain."""
        return f'{self.tag} {self.recipe}'


class Favorite(models.Model):
    """Describe a model which stores favorited recipes for a certain user."""

    favorite_recipe = models.ForeignKey(
        Recipe,
        verbose_name='Favorite recipe',
        help_text='Recipe which favorited by a certain user',
        on_delete=models.CASCADE,
        related_name='favorited_by',
    )
    user = models.ForeignKey(
        User,
        verbose_name='User',
        help_text='User who favorited a recipe',
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        """Describe settings for the Favorite model."""

        ordering = ('user', 'favorite_recipe')
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = (
            models.UniqueConstraint(
                fields=('favorite_recipe', 'user'),
                name='unique_favorite',
            ),
        )

    def __str__(self):
        """Show a favorite recipe for a certain user."""
        return f'Recipe {self.favorite_recipe} favorited by {self.user}'


class ShoppingCart(models.Model):
    """Describe a model which stores favorited recipes for a certain user."""

    recipe_in_cart = models.ForeignKey(
        Recipe,
        verbose_name='Recipe in cart',
        help_text='Recipe which added to cart by a certain user',
        on_delete=models.CASCADE,
        related_name='added_to_cart',
    )
    user = models.ForeignKey(
        User,
        verbose_name='User',
        help_text='User who added recipes to a cart',
        on_delete=models.CASCADE,
        related_name='cart',
    )

    class Meta:
        """Describe settings for the ShoppingCart model."""

        ordering = ('user', 'recipe_in_cart')
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping carts'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe_in_cart', 'user'),
                name='unique_good',
            ),
        )

    def __str__(self):
        """Show a tag - recipe chain."""
        return (
            f'Recipe {self.favorite_recipe} in shopping cart for {self.user}'
        )
