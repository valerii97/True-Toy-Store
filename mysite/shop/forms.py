from django import forms
from django.db.models import fields
from django.forms import widgets

from .models import Order, Delivery


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control order-input'

    class Meta:
        model = Order
        fields = ['name', 'email', 'phone']


class DeliveryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control delivery-input'

    class Meta:
        model = Delivery
        fields = ['city', 'street', 'house', 'appartment', 'post_office']
