from django.core.validators import MinValueValidator
from django.db import models


from users.models import CustomUser


class Tag(models.Model):
    Black = '#000000'
    White = '#ffffff'
    COLOR_HEX = (
        (Black, 'Black'),
        (White, 'White'),
        )
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Tag name')
    color = models.CharField(
        choices=COLOR_HEX,
        max_length=7,
        verbose_name='Tags color'
    )
    slug = models.SlugField(max_length=200, unique=True,
                            verbose_name='Unique slag',
                            )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_slug'
            )
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='ingredient name')
    measurement_unit = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(unique=True, max_length=200, verbose_name='recipe title')
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='recipe image',
        help_text='Recipe image',
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='recipe author', help_text='Recipe author',
    )
    text = models.TextField(
        help_text='Description of the recipe', verbose_name='recipe text',
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientsRecipe',
        related_name='recipes',
        verbose_name='list of ingredients',
        help_text='list of ingredients',
    )
    tags = models.ManyToManyField(
        Tag, through='TagsRecipe',
        related_name='recipes',
        help_text='Choose the tag',
    )
    cooking_time = models.PositiveSmallIntegerField(
        help_text='Cooking time, min',
        validators=[MinValueValidator(
            1, 'Cooking time could not be less than min'
        )],
    )
    pub_date = models.DateTimeField(
        'Created at', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text='Number of ingredients',
    )

    class Meta:
        verbose_name = 'Ingredient in recipe'
        verbose_name_plural = 'Ingredients in recipe'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe'
            )
        ]


class TagsRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite_recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=False, null=False,
        related_name='favorite_recipes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Shopping cart'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_cart'
            )
        ]
