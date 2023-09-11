from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Seller(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=255,unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self) -> str:
        return f"name: {self.name}, amount: {self.amount}"

class Orders(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self) -> str:
        return f"products: {self.products} amount: {self.amount}  products:{self.products}"

class PlatformApiCall(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    requested_url = models.URLField()
    requested_data = models.TextField()
    response_data = models.TextField()
