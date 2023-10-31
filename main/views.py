from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, DetailView
from registration.backends.default.views import ResendActivationView

from order.utils import cart_data
from .models import Category, Product
from .send_msg import activate_account


def home(request):
    products = Product.objects.order_by('-pk')
    data = cart_data(request)
    order = data['order']
    items = data['items']
    cart_items = data['cart_items']

    context = {
        'products': products,
        'order': order,
        'items': items,
        'cart_items': cart_items
    }

    # Пагинация
    # p = Paginator(products, 8)
    # page_num = request.GET.get('page', 1)
    # try:
    #     page = p.page(page_num)
    # except EmptyPage:
    #     page = p.page(1)

    return render(request, 'web/home.html', context)


def about_us(request):
    data = cart_data(request)
    order = data['order']
    items = data['items']
    cart_items = data['cart_items']

    context = {
        'order': order,
        'items': items,
        'cart_items': cart_items
    }
    return render(request, 'web/about.html', context=context)


class ProductList(ListView):
    model = Product
    template_name = 'web/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = self.kwargs['slug']
        queryset = Product.objects.filter(category=category)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cart_data(self.request)
        order = data['order']
        items = data['items']
        cart_items = data['cart_items']
        category = Category.objects.get(slug=self.kwargs['slug'])

        context.update({
            'category': category,
            'order': order,
            'items': items,
            'cart_items': cart_items
        })
        return context


class CategoryList(ListView):
    queryset = Category.objects.all()
    template_name = 'web/categories.html'
    context_object_name = 'categories'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cart_data(self.request)
        order = data['order']
        items = data['items']
        cart_items = data['cart_items']

        context.update({
            'order': order,
            'items': items,
            'cart_items': cart_items
        })
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'web/detail.html'
    context_object_name = 'pr'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cart_data(self.request)
        order = data['order']
        items = data['items']
        cart_items = data['cart_items']

        context.update({
            'order': order,
            'items': items,
            'cart_items': cart_items
        })
        return context


class CustomResendActivationView(ResendActivationView):
    def render_form_submitted_template(self, form):
        email = form.cleaned_data['email']
        context = {'email': email}
        return render(self.request,
                      'auth_user/resend_activation_complete.html',
                      context)


def auth_template(request):
    return render(request, 'auth_user/auth_account.html')



def not_found_page(request, exception):
    return render(request, 'errors/not-found.html', status=404)


def server_error_page(request, *args, **kwargs):
    return render(request, 'errors/errors-page.html', status=500)
