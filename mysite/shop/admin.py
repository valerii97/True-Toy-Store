from django.contrib import admin
from django.db import models

from .models import Product, OrderedProduct, Order, Customer, Category, Delivery, DeliveryService, DeliveryMethod, PaymentMethod, Payment

@admin.action(description='Mark selected orders as completed')
def order_completed(modeladmin, request, queryset):
    queryset.update(status='COM')


class OrderedProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'order_number', 'name', 'price', 'quantity', 'sum']

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_number', 'city', 'street', 'house', 'appartment', 'post_office', 'delivery_service']

class PaymentInline(admin.StackedInline):
    model = Payment

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        PaymentInline,
    ]
    list_display = ['id', 'name', 'email', 'phone', 'sum', 'date', 'status']
    ordering = ['date']
    actions= [order_completed]

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderedProduct, OrderedProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Customer)
admin.site.register(DeliveryMethod)
admin.site.register(DeliveryService)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(PaymentMethod)
admin.site.register(Payment)

