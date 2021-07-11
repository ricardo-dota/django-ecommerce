from django.contrib import admin

# Register your models here.

from  .models import Order, Payment , OrderProduct , OrderNotOrdered


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]
    
    class Meta:
        verbose_name = 'Orden Terminada'
        verbose_name_plural = 'Ordenes Terminadas'

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        return qs.filter(is_ordered=True)

class OrderAdminNotOrdered(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter  = ['status']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]
    
    def get_queryset(self, request):
        qs = super(OrderAdminNotOrdered, self).get_queryset(request)
        return qs.filter(is_ordered=False)

    class Meta:
        verbose_name = 'Orden no Terminada'
        verbose_name_plural = 'Ordenes no Terminadas' 



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderNotOrdered,OrderAdminNotOrdered)
admin.site.register(OrderProduct)
admin.site.register(Payment)