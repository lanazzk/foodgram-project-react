import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from recipe.models import Ingredient

PROJECT_DIR = Path(settings.BASE_DIR).resolve().joinpath('data')
FILE_TO_OPEN = PROJECT_DIR / 'ingredients.csv'


class Command(BaseCommand):
    help = 'Импорт ингредиентов в БД'

    def handle(self, **kwargs):
        with open(
            FILE_TO_OPEN, 'r', encoding='UTF-8'
        ) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
