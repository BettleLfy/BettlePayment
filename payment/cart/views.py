from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings

from goods.models import Item
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    product = get_object_or_404(Item, id=item_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    product = get_object_or_404(Item, id=item_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    template_name = 'cart/detail.html'
    stripe = settings.STRIPE_PUBLISHABLE_KEY
    cart = Cart(request)
    return render(request, template_name, {'cart': cart,
                                           'stripe_publishable_key': stripe})
