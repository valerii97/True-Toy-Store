from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.db import models
from django.db.models.deletion import CASCADE


class Category(models.Model):
    """Table for categories."""
    cat_name = models.CharField(max_length=255)

    def __str__(self):
        return self.cat_name


class Product(models.Model):
    """Table for products."""
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.FloatField()
    quantity = models.IntegerField(default=0, name="Quantity in stock")
    discount_price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='shop/images/')

    def __str__(self):
        return self.title


class Customer(models.Model):
    """Customers"""
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=30)
    is_registered = models.BooleanField(default=False)
    address = models.TextField(max_length=500)

    def __str__(self):
        return self.name


ORDER_STATUS_CHOICES = [
    ('NEW', 'New'),
    ('COM', 'Completed'),
    ('CAN', 'Canceled'),
]


class Order(models.Model):
    """Table for orders."""
    date = models.DateTimeField(default=timezone.now())
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=30)
    sum = models.FloatField()
    status = models.CharField(
        max_length=3, choices=ORDER_STATUS_CHOICES, default='NEW')

    def __str__(self):
        return 'Order#{}'.format(str(self.pk))


class DeliveryService(models.Model):
    """Choose delivery way"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=40)

    def __str__(self):
        return self.name


class DeliveryMethod(models.Model):
    delivery_service = models.ForeignKey(
        DeliveryService, on_delete=CASCADE, related_name='del_methods')
    to_post_office = models.BooleanField(verbose_name='На отделение')
    by_courier = models.BooleanField(verbose_name='Курьером')

    def __str__(self):
        return self.delivery_service.name


class Delivery(models.Model):
    """Order delivery"""
    order_number = models.ForeignKey(Order, on_delete=CASCADE)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255, null=True, blank=True)
    house = models.CharField(max_length=255, null=True, blank=True)
    appartment = models.CharField(max_length=255, null=True, blank=True)
    post_office = models.CharField(max_length=255, null=True, blank=True)
    delivery_service = models.CharField(max_length=100)

    def __str__(self):
        return str(self.order_number)


class OrderedProduct(models.Model):
    """Intermediate table"""
    product_id = models.ForeignKey(Product, on_delete=CASCADE)
    order_number = models.ForeignKey(Order, on_delete=CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()
    sum = models.FloatField()

    def __str__(self):
        return str(self.product_id)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

class Payment(models.Model):
    order_number = models.OneToOneField(Order, on_delete=CASCADE, primary_key=True)
    pay_method = models.CharField(max_length=100)

    def __str__(self):
        return str(self.order_number)