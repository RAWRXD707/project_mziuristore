from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    icon=models.ImageField(upload_to='category/', null=True,blank=True)
    
    class Meta:
        ordering=['name']
    
    def __str__(self):
        return f"{self.name}"
    
    def to_json(self):
        return {
            'id':self.id,
            'name':self.name,
            'description':self.description,
            'icon':self.icon.url if self.icon else None,
        }

    
class Model(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='model/', null=True, blank=True)

    class Meta:
        ordering=['name', 'price']

    def __str__(self):
        return f"{self.name}"
    
    def to_json(self):
        return{
            'id':self.id,
            'name':self.name,
            'description':self.description,
            'price': float(self.price),
            'category':self.category.to_json(),
            'image':self.image.url if self.image else None,
        }
    

def validate_file(file):
    max_size = 50 * 1024 * 1024  # 50MB

    if file.size > max_size:
        raise ValidationError("File too large")

    allowed_types = ['image/jpeg', 'image/png', 'video/mp4']
    if file.content_type not in allowed_types:
        raise ValidationError("Unsupported file type")
