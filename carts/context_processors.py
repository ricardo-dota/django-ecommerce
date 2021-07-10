from .models import Cart, CartItem
from carts.views import _cart_id
from django.http import HttpResponse

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter( cart_id = _cart_id(request) )
            #print('estoy antes del ifff')
            #print( list(cart[:1]))
            if request.user.is_authenticated:
                #print('estoy dentro del ')
                #print('----')
                cart_items  = CartItem.objects.all().filter(user = request.user)
            else:
                #cart_items  = CartItem.objects.all().filter(user = cart[:1])
                cart_items = CartItem.objects.all().filter( cart = cart[:1] )
                #print('estoy dentro del else')
                #print('----')
            for cart_item in cart_items:
                cart_count +=  cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict( cart_count = cart_count)