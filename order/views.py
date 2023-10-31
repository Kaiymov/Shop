from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView

import json

from main.models import Product
from main.send_msg import checkout_order_msg
from order.forms import ShippingAddressForm
from order.models import Order, OrderItem
from .utils import cart_data, guest_order


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def cart(request):
    data = cart_data(request)
    order = data['order']
    items = data['items']
    cart_items = data['cart_items']

    context = {
        'order': order,
        'items': items,
        'cart_items': cart_items,
    }
    return render(request, 'order/carts.html', context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    quantity = data['quantity']
    print(quantity)

    print('action:', action, 'productId:', product_id)

    user = request.user
    if user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id, status=True)
        order, created = Order.objects.get_or_create(customer=user, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = quantity

        orderItem.save()

        if action == 'remove':
            orderItem.delete()

    return JsonResponse('Продукт добавлен в корзину', safe=False)

def process_order(request):
    return JsonResponse('Payment complete', safe=False)


class Checkout(FormView):
    form_class = ShippingAddressForm
    template_name = 'order/checkout.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        data = form.save(commit=False)
        if self.request.user.is_authenticated:
            user = self.request.user
            email = user.email
            f_name = user.first_name

            order = Order.objects.get(customer=user, complete=False)
            items = order.orderitem_set.all()
        else:
            user, order, items, email, f_name = guest_order(self.request)

        order.complete = True
        order.save()

        data.customer = user
        data.order = order
        data.save()

        send_email_check = self.request.POST.get('send_email_check')
        if send_email_check:
            checkout_order_msg(email, f_name, order, items, data)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = cart_data(self.request)
        order = data['order']
        items = data['items']
        cart_items = data['cart_items']

        context = {
            'order': order,
            'items': items,
            'cart_items': cart_items
        }
        return context

    def dispatch(self, request, *args, **kwargs):
        data = cart_data(request)
        items = data['items']
        if len(items) == 0:
            return redirect(to='carts')
        return super().dispatch(request, *args, **kwargs)

def process_order(request):
    return JsonResponse('Payment Completed', safe=False)