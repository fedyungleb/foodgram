# Generated by Django 2.2.28 on 2024-10-08 18:46

from django.db import migrations
import json
import os

def load_data(apps, schema_editor):
    RecipesIngredient = apps.get_model('recipes', 'Ingredient')

    json_file_path = os.path.join(
        os.path.dirname(__file__),
        '../../data/ingredients.json'
    )

    json_file_path = os.path.abspath(json_file_path)

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        RecipesIngredient.objects.create(
            name=item['name'],
            measurement_unit=item['measurement_unit']
        )

class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220802_0922'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]