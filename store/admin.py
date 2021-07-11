from django.contrib import admin
from .models import Product,Variation, ProductGallery , CategoryCustom
import admin_thumbnails
from  .models import Category


#para dejarlo en el sectoer degaleria
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


# Register your models here.

@admin_thumbnails.thumbnail('images')
class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'product_naame', 'price_cash' , 'price_credit' , 'stock' , 'category' , 'modified_date')
    prepopulated_fields = { 'slug': ('product_naame',) }
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ( 'product', 'variation_category' , 'variaation_value' , 'is_active' )
    list_editable = ('is_active',)
    list_filter = ( 'product', 'variation_category' , 'variaation_value'  )

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('category_name',) }
    list_display = ('category_name','slug')



admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ProductGallery)
admin.site.register(CategoryCustom,CategoryAdmin)