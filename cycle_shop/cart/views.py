from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Cycle
from .cart import Cart
from .forms import CartAddProductForm

from django.urls import resolve

# @require_POST
# def cart_add(request, product_slug):
#     cart = Cart(request)
#     product = get_object_or_404(Cycle, slug=product_slug)
#     cart.add(product=product)
#     # if form.is_valid():
#     #     cd = form.cleaned_data
#     #     cart.add(product=product,
#     #              quantity=cd['quantity'],
#     #              update_quantity=cd['update'])
#     return redirect('shop:index')
@require_POST
def cart_add(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Cycle, slug=product_slug)
    cart.add(product=product)
    # if form.is_valid():
    #     cd = form.cleaned_data
    #     cart.add(product=product,
    #              quantity=cd['quantity'],
    #              update_quantity=cd['update'])

    return redirect('shop:show_cycle', cycle_slug=product_slug)


@require_POST
def cart_buy(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Cycle, slug=product_slug)
    form = CartAddProductForm(request.POST)
    cart.add(product=product)
    # if form.is_valid():
    #     cd = form.cleaned_data
    #     cart.add(product=product,
    #              quantity=cd['quantity'],
    #              update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_increase(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Cycle, slug=product_slug)
    cart.increase(product)
    return redirect('cart:cart_detail')


def cart_decrease(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Cycle, slug=product_slug)
    cart.decrease(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_remove(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Cycle, slug=product_slug)
    cart.remove(product)
    return redirect('cart:cart_detail')
