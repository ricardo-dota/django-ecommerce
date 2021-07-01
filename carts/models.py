from store.models import Product
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from .models import Product
from store.models import Variation

# Create your models here.

class Cart(models.Model):
    cart_id    = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product     = models.ForeignKey(Product , on_delete= models.CASCADE)
    variations  = models.ManyToManyField(Variation, blank= True)
    cart        = models.ForeignKey(Cart , on_delete= models.CASCADE)
    quantity    = models.IntegerField()
    is_active   = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price_credit * self.quantity

    def __unicode__(self):
        return self.product

