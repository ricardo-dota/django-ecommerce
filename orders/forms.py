from django import forms
from django.forms import fields
from .models import Order, Payment


class OrderForm( forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','email','address_line_1','address_line_2','country','state','city','order_note']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']