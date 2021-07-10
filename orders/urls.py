from store import views
from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order , name='place_order'),
    path('payments/',views.payments , name='payments'),
    #path('categoria/<slug:category_slug>/<slug:product_slug>', views.product_detail , name='products_detail'),
    #path('search/',views.search,name='search')
]
