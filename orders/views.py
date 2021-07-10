from store.models import Product
from django.shortcuts import render
from carts.models import CartItem
from django.shortcuts import get_object_or_404, redirect, render , get_object_or_404
from .forms import OrderForm,PaymentForm
from .models import Order, Payment , OrderProduct
from carts.models import CartItem
from store.models import Product
import datetime
from django.http import HttpResponse
import json


#verificacion del email 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests


# Create your views here.

def payments(request):

    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True 
    order.save()

    #mover el carro al dettale de la orden de productos
    cart_items = CartItem.objects.filter(user = request.user)


    for item in cart_items:
        orderproduct                = OrderProduct()
        orderproduct.order_id       = order.id
        orderproduct.payment        = payment
        orderproduct.user_id        = request.user.id
        orderproduct.product_id     = item.product_id
        orderproduct.quantity       = item.quantity
        orderproduct.product_price  = item.product.price_credit
        orderproduct.ordered        = True
        orderproduct.save()

        cart_item           = CartItem.objects.get(id=item.id)
        product_variation   = cart_item.variations.all()
        orderproduct        = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

    #reducir la cantidad de producto en el stock

        product = Product.objects.get( id = item.product_id )
        product.stock -= item.quantity
        product.save()

    #limpiar el carro

    CartItem.objects.filter( user = request.user).delete()

    #enviar email al cliente
    
    currennt_site = get_current_site(request)
    mail_subject = 'Por favor tu cuenta'
    message = render_to_string('orders/orden_recieved_email.html',{
                'user' : request.user,
                'order': order,
    })
    #enviamos el email

    to_email = request.user.email
    send_email = EmailMessage( mail_subject , message , to  = [ to_email ])
    send_email.send()
    
    #enviar orden  e indicar una reespuesta json

    return render(request, 'orders/payments.html')

#def confirm_order(request):


def place_order(request , total = 0 , quantity= 0 ):
    current_user = request.user

    #si el cart count es ,emps qie cero volver atras
    cart_items = CartItem.objects.filter( user = current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax         = 0

    for cart_item in cart_items:
        total           += ( cart_item.product.price_credit * cart_item.quantity)
        quantity        += cart_item.quantity

    tax = (2 * total )/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        #return HttpResponse(form.is_valid())
        #exit()
        if form.is_valid():

            #sotre the data en ñla tabla ordenes
            data                = Order()
            data.user           = current_user
            data.first_name     = form.cleaned_data['first_name']
            data.last_name      = form.cleaned_data['last_name']
            data.phone          = form.cleaned_data['phone']
            data.email          = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country        = form.cleaned_data['country']
            data.state          = form.cleaned_data['state']
            data.city           = form.cleaned_data['city']
            data.order_note     = form.cleaned_data['order_note']
            data.order_total    = grand_total
            data.tax            = tax
            data.ip             = request.META.get('REMOTE_ADDR')
            data.save()

            # generate order number
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d  = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get( user = current_user , is_ordered = False , order_number  = order_number )

            context = {
                'order'         : order,
                'cart_items'    : cart_items,
                'total'         : total,
                'tax'           :tax,
                'grand_total'   :grand_total
            }
            #return redirect('checkout')
            return render(request,'orders/payments.html',context)
    else:
        return redirect('checkout')        