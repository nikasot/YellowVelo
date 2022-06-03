from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<slug:product_slug>', views.cart_add, name='cart_add'),
    path('buy/<slug:product_slug>', views.cart_buy, name='cart_buy'),
    path('decrease/<slug:product_slug>', views.cart_decrease, name='cart_decrease'),
    path('increase/<slug:product_slug>', views.cart_increase, name='cart_increase'),
    path('remove/<slug:product_slug>', views.cart_remove, name='cart_remove'),
]