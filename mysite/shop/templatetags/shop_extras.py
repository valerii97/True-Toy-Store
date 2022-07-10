from django import template
from django.db.models import fields
from django.forms.widgets import TextInput

register = template.Library()

@register.simple_tag
def verbose_name(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name
