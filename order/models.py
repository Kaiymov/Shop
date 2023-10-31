import uuid

from django.db import models

from main.models import Product, CustomUser


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=True, null=True)
    transactoin_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitem = self.orderitem_set.all()
        for item in orderitem:
            if item.product.status is False:
                shipping = True
        return shipping


    @property
    def get_cart_total_price(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total_price for item in orderitem])
        return total

    @property
    def get_cart_items(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=10)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    COUNTRY_CHOISE = (
        ('kyrgyzstan',  'Кыргызстан'),
        ('kazahstan', 'Казахстан')
    )

    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200, choices=COUNTRY_CHOISE)
    zip_code = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

