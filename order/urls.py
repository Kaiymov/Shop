from django.urls import path

from .views import cart, process_order, update_item, Checkout

urlpatterns = [
    path('carts', cart, name='carts'),

    path('update_item/', update_item, name='update_item'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('process_order/', process_order, name='process_order'),

]