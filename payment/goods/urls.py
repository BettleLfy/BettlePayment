from django.urls import path

from .views import (
                    create_checkout_cart,
                    create_checkout_item, ProductListView,
                    ProductCreateView, ProductDetailView,
                    PaymentSuccessView, PaymentFailedView,
                    OrderHistoryListView)

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('item/<int:id>/', ProductDetailView.as_view(), name='item'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('history/', OrderHistoryListView.as_view(), name='history'),

    path('buy/<int:id>/', create_checkout_item,
         name='buy'),
    path('buy/', create_checkout_cart, name='buy-cart')
]
