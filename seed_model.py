from django.core.management.base import BaseCommand
from mziuristore.content.models import Model, Category
import json
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "model.jsonl")


def _parse_jsonl(path):
    data = []
    with open(path, "r") as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"error parsing jsonl: {str(e)}")
    return data


class Command(BaseCommand):
    help = "This command will populate database with Models"

    def add_arguments(self, parser):
        parser.add_argument("--seed", action="store_true")
        parser.add_argument("--delete", action="store_true")

    def handle(self, *args, **kwargs):

        if kwargs["delete"]:
            Model.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All models deleted"))
            return

        if not kwargs["seed"]:
            return

        models_data = _parse_jsonl(FILE_PATH)

        model_instances = []

        for item in models_data:
            try:
                category = Category.objects.get(name=item["category"])
                model_instances.append(
                    Model(
                        name=item["name"],
                        description=item["description"],
                        price=item["price"],
                        category=category,
                        image=item.get("image"),
                    )
                )
            except Category.DoesNotExist:
                self.stderr.write(
                    f"Category '{item['category']}' does not exist"
                )

        Model.objects.bulk_create(model_instances)

        self.stdout.write(
            self.style.SUCCESS(f"Created {len(model_instances)} models")
        )
