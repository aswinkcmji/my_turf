from django.db import models

# Create your models here.

class Products(models.Model):
    product_name = models.TextField(max_length=100, blank=False)
    price = models.FloatField(max_length=20, blank=False)
    quantity = models.IntegerField(blank=False,)
    # image_Link = models.ImageField()
    
    def __str__(self):
        return str(self.id)
