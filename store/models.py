from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    product_naame   = models.CharField(max_length=200,unique=True,verbose_name = "Titulo")
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500,blank=True,verbose_name = "Descripcion")
    price_cash      = models.IntegerField(verbose_name = "Precio Efectivo")
    price_credit    = models.IntegerField(verbose_name = "Precio Tarjeta de Credito")
    images          = models.ImageField(upload_to = 'photos/products' ,verbose_name = "Imagen" )
    stock           = models.IntegerField() 
    is_available    = models.BooleanField( default=True ,verbose_name = "Activado")
    category        = models.ForeignKey(Category , on_delete= models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   =  models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'productos'

    def get_url(self):
        return reverse('products_detail', args=[self.category.slug, self.slug]) 


    def __str__(self):
        return self.product_naame

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter( variation_category = 'color' , is_active = True )
    def sizes(self):
        return super(VariationManager, self).filter( variation_category = 'size' , is_active = True )

variation_category_choice = (
    ('color','color'),
    ('size', 'size' ),
) # tupla

class Variation(models.Model):
    product             = models.ForeignKey(Product , on_delete= models.CASCADE)
    variation_category  = models.CharField(max_length=100 , choices=variation_category_choice)
    variaation_value    = models.CharField(max_length=100)
    is_active           = models.BooleanField( default=True ,verbose_name = "Activado")
    created_date        = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()
    
    def __str__(self):
        return self.variaation_value


