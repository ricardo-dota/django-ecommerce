from django.contrib import admin
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'product_naame', 'price_cash' , 'price_credit' , 'stock' , 'category' , 'modified_date')
    prepopulated_fields = { 'slug': ('product_naame',) }


admin.site.register(Product,ProductAdmin)