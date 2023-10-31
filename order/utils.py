import json
from . models import *
from random_username.generate import generate_username

def cookie_cart(request):
    try:
        carts = json.loads(request.COOKIES['cart'])
    except Exception:
        carts = {}


    items = []
    order = {'get_cart_total_price': 0, 'get_cart_items': 0}
    cart_items = order['get_cart_items']

    for i in carts:
        try:
            cart_items += carts[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * carts[i]['quantity'])

            order['get_cart_total_price'] += total
            order['get_cart_items'] += carts[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'title': product.title,
                    'price': product.price,
                    'image': product.image
                },
                'quantity': carts[i]['quantity'],
                'get_total_price': total
            }
            items.append(item)
        except:
            pass
    return {'order': order, 'items': items, 'cart_items': cart_items}


def cart_data(request):
    if request.user.is_authenticated:
        user = request.user
        order, create = Order.objects.get_or_create(customer=user, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        order = cookie_data['order']
        items = cookie_data['items']
        cart_items = cookie_data['cart_items']

    return {'order': order, 'items': items, 'cart_items': cart_items}


def guest_order(request):
    print('COOKIES', request.COOKIES)

    email = request.POST.get('email')
    f_name = request.POST.get('first_name')
    phone = request.POST.get('phone-number')

    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    user, created = CustomUser.objects.get_or_create(
        email=email,
        username=generate_username(1)[0].lower(),
        first_name=f_name,
        phone=phone
    )

    order = Order.objects.create(
        customer=user,
        complete=False
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return user, order, items, email, f_name