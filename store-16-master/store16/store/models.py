from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Available_product(models.Model):
    price = models.DecimalField(max_digits=10,decimal_places=2)
    sellerName = models.CharField(max_length= 255, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)

class Wishlist(models.Model):
    products = models.ForeignKey('Product', on_delete=models.CASCADE, blank = True, null = True)
    user = models.ForeignKey(User, on_delete= models.CASCADE,blank = True, null = True)

class Product(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length= 255)
    publisher = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, default=None, blank = True, null = True)
    genre = models.CharField(max_length=255,default=None, blank = True, null = True)
    series = models.CharField(max_length=255, default=None, blank = True, null = True)
    rating = models.FloatField(default=None, blank = True, null = True)
    isbn = models.CharField(max_length =13)
    image = models.ImageField(upload_to='uploads/product/', default="defaultimage.gif", blank = True, null = True)
    abstract = models.CharField(max_length=510, blank= True, null = True)
    def __str__(self):
        return self.title    


class ShoppingCart(models.Model):
    books = models.ForeignKey(Available_product, on_delete= models.CASCADE)
    user = models.ForeignKey(User,null = True, on_delete= models.CASCADE)

class History(models.Model):
    books = models.ForeignKey(Product, on_delete= models.CASCADE)
    user = models.ForeignKey(User,null = True, on_delete= models.CASCADE)
    purchase_date = models.DateTimeField(default = timezone.now())

class Review(models.Model):
    username = models.CharField(max_length=255)
    rating = models.IntegerField(default=None)
    feedback = models.CharField(max_length=500, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
