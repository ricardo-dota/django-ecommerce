from django.core.checks import messages
from django.http.response import HttpResponse
from carts.models import CartItem
from django.shortcuts import get_object_or_404, render , redirect
from store.models import Product, ReviewRating
from category.models import Category
from carts.views import _cart_id
from django.http import HttpResponse
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from store.models import ProductGallery
from .forms import ReviewForm
# Create your views here.


def store(request, category_slug = None):
    categories = None 
    products   = None

    if category_slug != None:
        categories = get_object_or_404(Category , slug = category_slug )
        products = Product.objects.filter(category = categories , is_available = True).order_by('id')
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        product_count = products.count()

    paginator = Paginator( products , 2)
    page = request.GET.get( 'page')
    paged_products =  paginator.get_page(page)

    context = {
        'products' : paged_products,
        'product_count': product_count,
    }
    return render( request , 'store/store.html', context)

def product_detail(request,category_slug,product_slug):
    
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter( cart__cart_id = _cart_id(request) , product = single_product ).exists()

    except Exception as e:
        raise e

    product_gallery = ProductGallery.objects.filter( product = single_product.id)
    context = {
        'single_product':single_product,
        'in_cart' : in_cart,
        'product_gallery' :product_gallery
    }
    return render(request , 'store/product_detail.html',context)

def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            products = Product.objects.order_by('-created_date').filter( Q(description__icontains = keyword) | Q(product_naame__icontains  = keyword))
            product_count = products.count()
        else:
            return redirect('store')
    else:
        return redirect('store')
    context = {
        'products' : products,
        'product_count':product_count
    }
    return render( request , 'store/store.html',context)


def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER') # guarda la url de donde viene previamente
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get( user__id = request.user.id , product__id = product_id ) 
            form = ReviewForm( request.POST , instance = reviews ) # le pasamos la instancia pq si existe lo updatea
            form.save()
            messages.success( request , 'Gracias por tu Rewiew' )
            return redirect(url )
        except   ReviewRating.DoesNotExist:
            form = ReviewForm( request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                return redirect(url )
            else:
                return redirect(url )
    else:
        return redirect(url )