from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color_code = models.CharField(max_length=7, default='#49B64E')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Invalid character in category slug.')
        ])

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        default_related_name = 'tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Name',
        max_length=200)
    measurement_unit = models.CharField(
        'Measurement unit',
        max_length=200)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        verbose_name='Ingredient'
        )
    amount = models.PositiveSmallIntegerField(
        'Amount'
    )

    class Meta:
        verbose_name = 'Amount ingredients in recipe'
        verbose_name_plural = 'Amount ingredients in recipes'
        default_related_name = 'recipe_ingredients'
        ordering = ['id']

    def __str__(self):
        return (f'{self.ingredient.name} {self.ingredient.measurement_unit}'
                f'{self.amount}')


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='recipes',
        null=True
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        'Image',
        null=True,
        blank=True,
        upload_to='recipe/images',
        help_text='Add image'
    )
    text = models.TextField(
        verbose_name='Text',
        help_text='Add text'
    )
    ingredients = models.ManyToManyField(
        'IngredientInRecipe',
        related_name='recipes',
        verbose_name='Necessary ingredients'
    )
    tags = models.ManyToManyField(
        'Tag',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Cooking time in minutes',
        validators=[MinValueValidator(1, 'Value cannot be less than 1')],
        )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Recipe in favorite'
    )

    class Meta:
        verbose_name = 'Favorite recipes'
        UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite'
        )


class Shopping_list(models.Model):
    user = models.ForeignKey(
        User,
        related_name='shopping_list',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_list',
        on_delete=models.CASCADE,
        verbose_name='Recipe in shopping_list'
    )

    class Meta:
        verbose_name = 'Shopping list'
        UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_shopping_list'
        )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta():
        UniqueConstraint(
            fields=['user', 'following'],
            name='unique_follow'
        )

    def __str__(self):
        return self.following.username
