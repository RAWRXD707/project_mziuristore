from django.contrib import admin
from .models import Category, Model, Product  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']

    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" />'
        return "No Image"

    preview.allow_tags = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    list_filter=['name']
    search_fields = ['name', 'description']

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    list_filter=['name', 'category', 'price']
    search_fields = ['name', 'description']
