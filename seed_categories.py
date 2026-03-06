from django.core.management.base import BaseCommand
from apps.content.models import Category
from apps.content.serializers import CategoryCreateSerializer
import json
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "category.jsonl")


def _parse_jsonl(path):
    data = []
    with open(path, 'r') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"error parsing jsonl: {str(e)}")
    return data


class Command(BaseCommand):
    help = "This command will populate database with Categories"

    def add_arguments(self, parser):
        parser.add_argument("--seed", action="store_true")
        parser.add_argument("--delete", action="store_true")

    def handle(self, *args, **kwargs):

        if kwargs['delete']:
            Category.objects.all().delete()
            return

        categories_data = _parse_jsonl(FILE_PATH)

        serializer = CategoryCreateSerializer(data=categories_data, many=True)
        if not serializer.is_valid():
            self.stderr.write(str(serializer.errors))
            return
        
        Category.objects.bulk_create([
            Category(**item) for item in serializer.validated_data
        ])

        self.stdout.write(self.style.SUCCESS(f"Created {len(serializer.validated_data)} categories"))
