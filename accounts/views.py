from orders.models import Order
from carts.views import _cart_id
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm , UserForm , UserProfileForm
from .models import Account,UserProfile
from django.http import HttpResponse
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from orders.models import Order
from carts.views import _cart_id
#verificacion del email 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests
# Create your views here.



def register(request):
    #comprobamos si se envio algo
    if request.method == 'POST':
        form  =  RegistrationForm(request.POST)
        if form.is_valid():
            first_name      = form.cleaned_data['first_name']
            last_name       = form.cleaned_data['last_name'] 
            email           = form.cleaned_data['email']
            phone_number    = form.cleaned_data['phone_number'] 
            password        = form.cleaned_data['password']
            username        = email.split("@")[0]
            user = Account.objects.create_user( first_name = first_name, last_name= last_name , email =  email  , username = username,password = password)
            user.phone_number = phone_number
            user.ip_address   = request.META.get('REMOTE_ADDR')
            user.save()


            #  ccreamos el user prfile 
            profile         = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default.png'
            profile.save()



             

            #http://{{ domain }}{% url 'activate' uidb64=uid token=token %}

            #user activacion 
            currennt_site = get_current_site(request)
            mail_subject = 'Por favor tu cuenta'
            message = render_to_string('accounts/account_verification_email.html',{
                'user' : user,
                'domain' : currennt_site,
                'uidb64d' : urlsafe_base64_encode(force_bytes(user.pk)), #vamos codificar el pk del usuario 
                'token': default_token_generator.make_token(user), 

            })
            #enviamos el email
            to_email = email
            send_email = EmailMessage( mail_subject , message , to  = [ to_email ])
            send_email.send()

            #messages.success(request, 'Gracias por registrarse con nosotros. Te hemos enviado un email para verificar')
            return redirect('/accounts/login/?command=verification&email='+email)
        else:
            messages.error(request, 'Tu Formulario contiene Errores')
            #exit()
    else:
        form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request,'accounts/register.html',context)

def login(request):

    #if auth.authenticate:
        #return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate( email = email , password = password )
        if user is not None:

            try:
                #print('entrando al try')
                cart = Cart.objects.get( cart_id = _cart_id(request) )
                is_cart_item_exists = CartItem.objects.filter(  cart = cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter( cart= cart)

                    #optime el variation del producto
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append( list( variation) )
                    #obtenemos los item del carro desde el usuario para acceder a als variaciones
                    cart_item = CartItem.objects.filter(user = user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id) 
                    
                   # product_variation = [1,2,3,4,5,6]
                   # ex_var_list = [4,5,3,5]
                    for pr in product_variation:
                        if pr in ex_var_list:
                             index = ex_var_list.index(pr)
                             item_id = id[index]
                             item = CartItem.objects.get(id = item_id)
                             item.quantity += 1
                             item.user = user
                             item.save()  
                        else:
                            cart_item = CartItem.objects.filter( cart = cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                #print('entrando al exceptin')
                pass

            auth.login(request, user)
            messages.success( request , 'Estas logeado')
            url = request.META.get('HTTP_REFERER')#graba la url que vienes anteiormente
            try:
                query = requests.utils.urlparse(url).query #
                #next=/cart/checkout/
                params = dict( x.plit('=') for x in query.split('&'))
                if 'next' in params:
                    nextPAge = params['next']
                    return redirect(nextPAge)
            except:      
                return redirect('dashboard')
        else:
            messages.error( request , 'Credenciales invalidas')
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required( login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'Tu sesion ha terminado')
    return redirect('login')


def activate(request , uidb64d , token):
    try:
        uid = urlsafe_base64_decode(uidb64d).decode()
        user = Account._default_manager.get( pk = uid)
    except( TypeError , ValueError , OverflowError , Account.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token( user, token):
        user.is_active = True
        user.save()
        messages.success( request , 'Felicidades haz activbado tu cuenta.')
        return redirect('login')
    else:
        messages.error( request , 'Activacion invalida.')
        return redirect('register') 

@login_required(login_url='/login/')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter( user_id = request.user.id , is_ordered = True)
    orders_count = orders.count()
    
    userprofile = UserProfile.objects.get( user_id = request.user.id )
                
    context = {
        'orders':orders,
        'orders_count':orders_count,
        'userprofile'  : userprofile,
    }
    return render(request,'accounts/dashboard.html',context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter( email = email).exists():
            user = Account.objects.get( email__exact = email)

            #reseteamos el password
            currennt_site = get_current_site(request)
            mail_subject = 'Resetea tu Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user' : user,
                'domain' : currennt_site,
                'uidb64d' : urlsafe_base64_encode(force_bytes(user.pk)), #vamos codificar el pk del usuario 
                'token': default_token_generator.make_token(user), 

            })
            #enviamos el email
            to_email = email
            send_email = EmailMessage( mail_subject , message , to  = [ to_email ])
            send_email.send()

            messages.success( request , 'Link para resetear tu password enviado a tu email')
            return redirect('login')

        else:
            messages.error( request, 'El usuario no existe' )
            return redirect('forgotPassword')


    return render(request,'accounts/forgotPassword.html') 

def resetpassword_validate(request , uidb64d , token):
    try:
         uid = urlsafe_base64_decode(uidb64d).decode()
         user = Account._default_manager.get(pk = uid)
    except( TypeError , ValueError , OverflowError , Account.DoesNotExist):
        user = None     

    if user is not None and default_token_generator.check_token( user, token):
        request.session['uid']  = uid
        messages.success(request,'Por favor resetea tu password')
        return redirect('resetPassword')
    else:
        messages.error( request , 'Este link sera expirado' )
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password          = request.POST['password'] 
        confirm_password  = request.POST['confirm_password'] 
        if password  == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get( pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request , 'Passsword reseteado correctamente')
            return redirect('login')
        else:
            messages.error(request,'Los password no son iguales')
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')

@login_required(login_url='/login/')
def my_orders(request):
    orders = Order.objects.filter( user = request.user , is_ordered = True)
    context = {
        'orders':orders
    }
    return render(request,'accounts/my_orders.html',context) 

@login_required(login_url='/login/')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url='/login/')
def change_password(request):

  if request.method == 'POST':
    current_password      = request.POST['current_password']
    new_password          = request.POST['new_password']
    confirm_new_password  = request.POST['confirm_new_password']
    
    user = Account.objects.get( username__exact = request.user.username )

    if new_password == confirm_new_password:
        success = user.check_password(current_password)
        if success:
            user.setpassword(new_password)
            user.save()
            #auth.logout(request)
            messages.success( request , 'Password updateado correctamente')
            return redirect('change_password')
        else:
            messages.error( request , 'Por favor ingresa los datos correctos')
            return redirect('change_password')
    else:
        messages.error( request , 'Los password no son iguales')
        return redirect('change_password')

  return render (  request,'accounts/change_password.html' )

def order_detail(request, order_id):
    
    try:
        order = Order.objects.get( order_number = order_id, user = request.user , is_ordered = True)
    except( Order.DoesNotExist):
        return redirect('dashboard')

    context = {
        'order':order
    }
    return render(request,'accounts/order_detail.html',context) 