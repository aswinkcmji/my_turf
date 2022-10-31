from django.db import models

# Create your models here.


class ProductsModel(models.Model):
    product_name = models.TextField(max_length=100, blank=False)
    price = models.FloatField(max_length=20, blank=False)
    quantity = models.IntegerField(blank=False,)
    image = models.ImageField(upload_to='images')
    
    def __str__(self):
        return str(self.id)


class CartModel(models.Model):
    username = models.TextField(max_length=100, blank=False)
    product_id = models.IntegerField(blank=False )
    product_name = models.TextField(max_length=100, blank=False)
    price = models.FloatField(blank=False)
    quantity = models.IntegerField(blank=False,)
    image = models.TextField(max_length=100, blank=False)

    
    def __str__(self):
        return str(self.id)

class CheckoutModel(models.Model):

    orderno = models.IntegerField(blank=False)
    username = models.TextField(max_length=100, blank=False)
    product_id = models.TextField(blank=False )
    product_name = models.TextField(max_length=100, blank=False)
    price = models.TextField(blank=False)
    quantity = models.TextField(blank=False,)
    image = models.TextField(max_length=100, blank=False)

    def __str__(self):
        return str(self.id)