from django.core import exceptions
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render , get_object_or_404
from . import views
from .models import CartItem, Product,Cart
from store.models import Variation
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

#funcion privada
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# Create your views here.
def add_cart(request, product_id):

    #color = request.POST.get('color')
    #size = request.GET.get('size')
    #return HttpResponse(color)
    #exit()
    product = Product.objects.get( id = product_id) # obtener el producto
    product_vartion = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value =  request.POST[key]
            try:
                # iexact toma el valor sin importar que sea low o cap
                variation = Variation.objects.get( product = product,  variation_category__iexact = key , variaation_value__iexact = value )
                product_vartion.append(variation)
                
            except:
                pass

        #color = request.POST['color']
        #size = request.POST['size']
        #return HttpResponse(product_vartion)
        #exit()
    try:
        cart = Cart.objects.get( cart_id = _cart_id(request)  ) #obtiene el carro usando el id de la session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    is_cart_item_exists = CartItem.objects.filter( product = product , cart = cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter( product = product,  cart = cart)
        # variblaes si exiten 
        #variation actuales
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        if product_vartion in ex_var_list:
            #incrementamos la cantidad delk carro 
            index = ex_var_list.index(product_vartion)
            item_id = id[index]
            item = CartItem.objects.get(product = product, id = item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create( product = product , quantity = 1 , cart = cart )
            if len(product_vartion) > 0:
                item.variations.clear()
                item.variations.add(*product_vartion)
                item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.variations.clear()
        if len(product_vartion) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_vartion)
        cart_item.save()
    #return HttpResponse(cart_item.product)
    #exit()
    return redirect('cart')

def remove_cart(request,product_id ,cart_item_id):
    cart = Cart.objects.get( cart_id = _cart_id(request))  
    product = get_object_or_404( Product , id = product_id)
    try:
        cart_item = CartItem.objects.get( product = product , cart = cart , id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    cart = Cart.objects.get( cart_id = _cart_id(request))  
    product = get_object_or_404( Product , id = product_id)
    cart_item = CartItem.objects.get( product = product , cart = cart , id = cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request , total = 0 , quantity = 0 , cart_items = None):
    try:
        tax = 0 
        grand_total = 0
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter( cart = cart , is_active = True)
        for cart_item in cart_items:
            total    += ( cart_item.product.price_credit * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total )/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass
    
    context = {
        'total' : total ,
        'quantity':quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total' : grand_total

    }
    return render(request,'store/cart.html',context)
