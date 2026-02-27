from ninja import Router, Schema
from .models import Category, Model

router = Router()

@router.get("categories", response=list[CategoryOut])
def get_categories(request, contain: str = None):
    categories = Category.objects.all()

    if contain is not None:
        categories = categories.filter(name__icontains=contain)

    return categories

@router.get("models", response=list[ModelOut])
def get_models(request, min_price: int = None, max_price: int = None, category : str = None):
    models = Model.objects.all()
    
    if min_price is not None:
        models = models.filter(price__gte=min_price)
    
    if max_price is not None:
        models = models.filter(price__lte=max_price)

    if category is not None:
        models = models.filter(category__name=category)

    return models

@router.post("create_category", response=CategoryOut)
def create_category(request, data: CategoryIn):
    category = Category.objects.create(name=data.name, description=data.description, icon=data.icon)
    return category

@router.post("create_model", response=ModelOut)
def create_model(request, data: ModelIn):
    model = Model.objects.create(name=data.name, description=data.description, price=data.price, category=Category.objects.get(name=data.category), image=data.image)
    return model
