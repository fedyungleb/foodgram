from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=10,
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет тега',
        unique=True
    )
    slug = models.SlugField(
        max_length=10,
        unique=True
    )
