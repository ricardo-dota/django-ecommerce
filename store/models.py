from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from category.models import Category
from accounts.models import Account
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
        verbose_name = '1. Producto'
        verbose_name_plural = '1. Productos'

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

    class Meta:
        verbose_name  = '4. Combinacion'
        verbose_name_plural  = '4. Combinaciones'

    def __str__(self):
        return self.variaation_value


class ProductGallery(models.Model):
    product         = models.ForeignKey( Product , default=None , on_delete=CASCADE)
    image           = models.ImageField(upload_to = 'store/products' ,max_length= 255 ,verbose_name = "foto" )
    created_date    = models.DateTimeField(auto_now_add=True)

    def __Str__(self):
        return self.product.product_naame
    
    class Meta:
        verbose_name  = '3. Galeria de Producto'
        verbose_name_plural  = '3. Galeria de Productos'

class CategoryCustom(Category):
    class Meta:
        proxy = True
        verbose_name = '2. Categoria'
        verbose_name_plural = '2. Categorias'


class ReviewRating(models.Model):
    product         = models.ForeignKey( Product , on_delete= models.CASCADE)
    user            = models.ForeignKey( Account , on_delete= models.CASCADE)
    subject         = models.CharField( max_length = 100 , blank= True )
    review          = models.TextField( max_length=500 , blank=True)
    rating          = models.FloatField( )
    ip              = models.CharField( max_length=20 , blank= True )
    status          = models.BooleanField( default= True)
    created_date    = models.DateTimeField(auto_now_add=True)  
    updated_at      = models.DateTimeField(auto_now_add=True)  


    def __str__(self):
        return self.subject


