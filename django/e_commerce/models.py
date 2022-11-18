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
    price = models.FloatField(default=0.0,blank=False)
    quantity = models.IntegerField(blank=False,)
    image = models.TextField(max_length=100, blank=False)
    date=models.DateField(blank=True,null=True)
    status = models.TextField(blank=True,default="Awaiting Fulfillment")

    def __str__(self):
        return str(self.id)


class BillingAddressModel(models.Model):

    username = models.TextField(max_length=100, blank=False)
    firstname = models.TextField(blank=False )
    contactnumber = models.BigIntegerField(blank=False)
    houseno = models.TextField(default=0.0,blank=False)
    landmark = models.TextField(blank=False,)
    location = models.TextField(max_length=100, blank=False)
    state = models.TextField(blank=True,null=True)
    pincode = models.IntegerField(max_length=100, blank=False)

    def __str__(self):
        return str(self.id)

