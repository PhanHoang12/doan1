from django.db import models
from country.models import CustomUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Brand(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete= models.SET_NULL,null=True )
    sale = models.IntegerField(default=0)
    company_profile = models.CharField(max_length=255, blank=True)
    images = models.TextField(blank=True)
    detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return self.name