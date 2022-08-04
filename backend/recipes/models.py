from django.core.validators import MinValueValidator
from django.db import models

from colorfield.fields import ColorField

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        verbose_name='название тега',
        max_length=200,
        unique=True
    )
    color = ColorField(
        default='#FF0000',
        max_length=7,
        verbose_name='Цвет тега',
        unique=True
    )
    slug = models.SlugField(
        verbose_name='поле слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        constraints = (
            models.UniqueConstraint(
                fields=('slug',),
                name='unique_slug'
            ),
        )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='ingredient name'
    )
    measurement_unit = models.CharField(
        'величина измерения',
        max_length=10
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='recipe title')
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='recipe image',
        help_text='Картинка рецепта',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='recipe author',
        help_text='Автор рецепта',
    )
    text = models.TextField(
        help_text='Текстовое описание рецепта',
        verbose_name='recipe text',
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientsRecipe',
        related_name='recipes',
        verbose_name='list of ingredients',
        help_text='Список ингредиентов',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagsRecipe',
        related_name='recipes',
        verbose_name='выбор тега',
        help_text='Выберите тэг',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='время готовки',
        help_text='Время приготовления, мин',
        validators=[MinValueValidator(
            1, 'Время приготовления не может быть меньше 1 мин'
        )],
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='ингридиенты в рецепте'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='рецепт ингридиенты'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(
            1, 'Количество не может быть меньше 1 мин'
        )],
        help_text='Количество ингредиента',
        verbose_name='количество'
    )

    class Meta:
        verbose_name = 'Ingredient in recipe'
        verbose_name_plural = 'Ingredients in recipe'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='unique_recipe'
            ),
        )


class TagsRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='тэг рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт тэга'
    )


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='юзер избранное'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=False, null=False,
        related_name='favorite_recipes',
        verbose_name='избранный рецепт'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_favorite'
            ),
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='список покупок пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='список покупок'
    )

    class Meta:
        verbose_name = 'Shopping cart'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_cart'
            ),
        )
