from django.views.decorators.http import require_POST
from django.http.response import (HttpResponseNotFound,
                                  JsonResponse)
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, TemplateView
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

from cart.cart import Cart
from .models import Item, Order
from cart.forms import CartAddProductForm


class ProductListView(ListView):
    model = Item
    template_name = 'payments/product_list.html'
    context_object_name = 'product_list'


@method_decorator(staff_member_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Item
    fields = '__all__'
    template_name = 'payments/product_create.html'
    success_url = reverse_lazy('goods:home')


class ProductDetailView(DetailView):
    model = Item
    template_name = 'payments/product_detail.html'
    pk_url_kwarg = 'id'

    # def product_detail(self, request, id):
    #     item = get_object_or_404(Item,
    #                              pk=id,
    #                              available=True)
    #     cart_product_form = CartAddProductForm()
    #     return render(request, self.template_name,
    #                   {'item': item,
    #                    'cart_product_form': cart_product_form})

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['cart_product_form'] = CartAddProductForm()
        return context


@csrf_exempt
def create_checkout_item(request, id):
    item = get_object_or_404(Item, pk=id)
    cart = [
        {
            'product': item,
            'price': item.price,
            'quantity': 1,
            'total_price': item.price,
        }
    ]
    return create_checkout_session(request, cart)


def create_checkout_session(request, cart):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    request_data = json.loads(request.body)
    order = Order()
    order.customer_email = request_data['email']
    order.amount = sum(map(lambda item: item['total_price'] * 100, cart))
    order.save()
    order.items.add(*list(map(lambda x: x['product'], cart)))

    checkout_session = stripe.checkout.Session.create(
        customer_email=request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['product'].name,
                        },
                    'unit_amount': int(item['price'] * 100),
                    },
                'quantity': item['quantity'],
            } for item in cart
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('goods:success')
        ) + f"?order_id={order.id}",
        cancel_url=request.build_absolute_uri(reverse('goods:failed')),
    )

    return JsonResponse({'sessionId': checkout_session.id})


@csrf_exempt
@require_POST
def create_checkout_cart(request):
    cart = Cart(request)
    return create_checkout_session(request,
                                   cart)


class PaymentSuccessView(TemplateView):
    template_name = 'payments/payment_success.html'

    def get(self, request, *args, **kwargs):
        order_id = request.GET.get('order_id')
        if order_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY

        order = get_object_or_404(Order,
                                  pk=order_id)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)


class PaymentFailedView(TemplateView):
    template_name = 'payments/payment_failed.html'


@method_decorator(staff_member_required, name='dispatch')
class OrderHistoryListView(ListView):
    model = Order
    template_name = 'payments/order_history.html'
