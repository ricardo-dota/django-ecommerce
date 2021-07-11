from django.db import models
from accounts.models import Account
from store.models import Product, Variation

# Create your models here.
class Payment( models.Model):

    PAYMENT_METHODS = (
        ('PayPAL', 'PayPAL'),
        ('TRANSFER', 'TRANSFER'),
        ('WEBPAY', 'WEBPAY')
    )

    user            = models.ForeignKey( Account , on_delete=models.CASCADE )
    payment_id      = models.CharField( max_length= 100)
    payment_method  = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='TRANSFER')
    amount_paid     = models.CharField( max_length= 100)
    status          = models.CharField( max_length= 100)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '3. Pago'
        verbose_name_plural = '3. Pagos'

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user            = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number    = models.CharField(max_length=20)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    phone           = models.CharField(max_length=15)
    email           = models.EmailField(max_length=50)
    address_line_1  = models.CharField(max_length=50)
    address_line_2  = models.CharField(max_length=50, blank=True)
    country         = models.CharField(max_length=50)
    state           = models.CharField(max_length=50)
    city            = models.CharField(max_length=50)
    order_note      = models.CharField(max_length=100, blank=True)
    order_total     = models.FloatField()
    tax             = models.FloatField()
    status          = models.CharField(max_length=10, choices=STATUS, default='New')
    ip              = models.CharField(blank=True, max_length=20)
    is_ordered      = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '1. Orden Terminada'
        verbose_name_plural = '1. Ordenes Terminadas'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.order_number


class OrderNotOrdered(Order):
    class Meta:
        proxy = True
        verbose_name = '2. Orden No Terminada'
        verbose_name_plural = '2. Ordenes No Terminadas'

class OrderProduct(models.Model):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations      = models.ManyToManyField(Variation, blank=True)
    quantity        = models.IntegerField()
    product_price   = models.FloatField()
    ordered         = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_naame

    class Meta:
        verbose_name = '4. Producto en la Orden'
        verbose_name_plural = '4. Productos en la Orden'

