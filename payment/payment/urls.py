from django.contrib import admin
from django.urls import include, path, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('', include(('goods.urls', 'goods'), namespace='goods'))
]
