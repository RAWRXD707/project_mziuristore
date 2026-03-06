import csv
import json
from collections import defaultdict
from django.core.management.base import BaseCommand
from mziuristore.content.models import Product


class Command(BaseCommand):
    help = "Export product catalog grouped by category"

    def add_arguments(self, parser):
        parser.add_argument(
            "--format",
            type=str,
            choices=["csv", "json"],
            required=True,
            help="Output format: csv or json",
        )

        parser.add_argument(
            "--output",
            type=str,
            help="Output file name (optional for JSON)",
        )

        parser.add_argument(
            "--category",
            type=str,
            help="Filter by category name",
        )

    def handle(self, *args, **options):
        output_format = options["format"]
        output_file = options["output"]
        category_filter = options["category"]

        queryset = Product.objects.select_related("category")

        if category_filter:
            queryset = queryset.filter(category__name=category_filter)

        grouped_data = self.group_by_category(queryset)

        if output_format == "csv":
            if not output_file:
                self.stderr.write("CSV export requires --output filename")
                return
            self.export_csv(grouped_data, output_file)

        elif output_format == "json":
            filename = output_file or "catalog.json"
            self.export_json(grouped_data, filename)

        self.stdout.write(self.style.SUCCESS("Export completed successfully."))

    def group_by_category(self, queryset):
        grouped = defaultdict(list)

        for product in queryset:
            grouped[product.category.name].append({
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
            })

        return grouped

    def export_csv(self, grouped_data, filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Product ID", "Product Name", "Price"])

            for category, products in grouped_data.items():
                for product in products:
                    writer.writerow([
                        category,
                        product["id"],
                        product["name"],
                        product["price"],
                    ])

    def export_json(self, grouped_data, filename):
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(grouped_data, file, indent=4)
