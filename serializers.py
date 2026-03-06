from rest_framework import serializers
from .models import Category, Model


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    icon = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class ModelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    category = serializers.CharField()
    image = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data):
        category_name = validated_data.pop("category")
        category = Category.objects.get(name=category_name)
        return Model.objects.create(category=category, **validated_data)

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "description": instance.description,
            "price": instance.price,
            "category": {
                "id": instance.category.id,
                "name": instance.category.name,
                "description": instance.category.description,
                "icon": instance.category.icon,
            },
            "image": instance.image,
        }
