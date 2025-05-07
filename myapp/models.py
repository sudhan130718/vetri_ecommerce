

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Brands(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField()

    def __str__(self):
        return self.name    


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand=models.ForeignKey(Brands,on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    position = models.IntegerField()

    def __str__(self):
        return self.name    

    


class Users(models.Model):
    name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)


    def __str__(self):
        return self.name    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def total(self):
        return sum(item.total_price() for item in self.cartitem_set.all())
    

    


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
# Order

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField()
    status = models.CharField(max_length=50, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='cod')  # Set default here
    cardholder_name = models.CharField(max_length=100, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    expiry_date = models.CharField(max_length=5, null=True, blank=True)
    cvv = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Assuming Product model exists
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"