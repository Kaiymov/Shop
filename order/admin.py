from django.contrib import admin

from .models import Order, OrderItem, ShippingAddress

admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(ShippingAddress)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'zip_code', 'country', 'date_added')
    list_display_links = ('id', 'customer', 'order', 'zip_code')
    search_fields = ('customer', 'id', 'country')
    # list_editable = ('status',)
    list_filter = ('customer', 'country',)
