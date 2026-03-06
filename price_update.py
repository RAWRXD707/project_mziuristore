from django.core.management.base import BaseCommand
from mziuristore.content.models import Product


class Command(BaseCommand):
    help = "Apply percentage price change to a category"

    def add_arguments(self, parser):
        parser.add_argument("--category", required=True)
        parser.add_argument("--percent", type=float, required=True)

    def handle(self, *args, **options):
        category_name = options["category"]
        percent = Decimal(str(options["percent"]))

        products = Product.objects.filter(category__name=category_name)

        if not products.exists():
            self.stdout.write(self.style.WARNING("No products found."))
            return

        for product in products:
            change = product.price * (percent / 100)
            product.price += change
            product.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {products.count()} products in {category_name}"
            )
        )
