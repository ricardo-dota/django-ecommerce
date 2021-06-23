from django.db import models
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

