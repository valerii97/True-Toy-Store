import json

from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.core.mail import send_mail
from django.db.models.fields import BooleanField

from .models import Category, DeliveryService, Product, OrderedProduct, Order, DeliveryMethod, PaymentMethod, Payment
from .forms import OrderForm, DeliveryForm
from .mail import send_order_email
from .telegr import telbot_send_msg


class IndexView(generic.ListView):
    """This view is for home page."""
    model = Product
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryView(generic.DetailView):
    """This view is for categories pages."""
    model = Category
    template_name = 'shop/category.html'


class DetailView(generic.DetailView):
    """This view will show details of chosen product."""
    model = Product
    template_name = 'shop/product_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


def add_to_cart(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(pk=product_id)

    if product.discount_price:
        pr = {
            'product_quantity': 1,
            'title': product.title,
            'price': product.discount_price,
            'image': product.image.url,
            'cost': product.discount_price,
        }
    else:
        pr = {
            'product_quantity': 1,
            'title': product.title,
            'price': product.price,
            'image': product.image.url,
            'cost': product.price,
        }
    s = request.session
    # s.clear()
    # adding products in cart
    # cheking if we already added any product to cart
    if 'cart' in s.keys():
        # checking if we already added product with this id
        if product_id in s['cart']:
            # if yes, than just increase it's quantity and cost
            s['cart'][product_id]['product_quantity'] += 1
            s['cart'][product_id]['cost'] = s['cart'][product_id]['price'] * \
                s['cart'][product_id]['product_quantity']

        # if no product with this id in cart, than adding product details
        else:
            s['cart'][product_id] = pr
        # saving session on change of s['cart']
        s.modified = True
    # if no products are in cart, creating session key 'cart' and assigning
    # with dict of id and selected product details (title, quantity, price, image)
    else:
        s['cart'] = {product_id: pr}

    if 'total_cart_quantity' not in s.keys():
        s['total_cart_quantity'] = 0
    s['total_cart_quantity'] += 1
    if 'total_cart_sum' not in s.keys():
        s['total_cart_sum'] = 0
    s['total_cart_sum'] += s['cart'][product_id]['price']

    return render(request, 'shop/cart.html', {
        'cart_products': s['cart'],
        'total_cart_quantity': s['total_cart_quantity'],
        'total_cart_sum': s['total_cart_sum'],
    })


def clear_cart(request):
    s = request.session
    del s['cart']
    del s['total_cart_quantity']
    del s['total_cart_sum']
    return render(request, 'shop/cart.html', {
        'cart_products': {},
        'total_cart_quantity': 0,
        'total_cart_sum': 0,
    })


def open_cart(request):
    s = request.session

    if 'cart' in s.keys():
        cart = s['cart']
    else:
        cart = {}

    if 'total_cart_quantity' in s.keys():
        tot_cart_quan = s['total_cart_quantity']
    else:
        tot_cart_quan = 0

    if 'total_cart_sum' in s.keys():
        tot_cart_sum = s['total_cart_sum']
    else:
        tot_cart_sum = 0

    return render(request, 'shop/cart.html', {
        'cart_products': cart,
        'total_cart_quantity': tot_cart_quan,
        'total_cart_sum': tot_cart_sum,
    })


def delete_item_fm_cart(request):
    s = request.session
    item_id = request.GET.get('id')

    if item_id in s['cart']:
        quantity = s['cart'][item_id]['product_quantity']
        cost = s['cart'][item_id]['cost']
        del s['cart'][item_id]

    s['total_cart_quantity'] -= quantity
    s['total_cart_sum'] -= cost

    return render(request, 'shop/cart.html', {
        'cart_products': s['cart'],
        'total_cart_quantity': s['total_cart_quantity'],
        'total_cart_sum': s['total_cart_sum'],
    })


def substruct_fm_cart(request):
    s = request.session
    item_id = request.GET.get('id')

    if item_id in s['cart']:
        if s['cart'][item_id]['product_quantity'] > 1:
            s['cart'][item_id]['product_quantity'] -= 1
            price = s['cart'][item_id]['price']
            s['cart'][item_id]['cost'] -= price
        else:
            price = s['cart'][item_id]['price']
            del s['cart'][item_id]
        s['total_cart_quantity'] -= 1
        s['total_cart_sum'] -= price
    else:
        print("There is no such product in the cart")
    return render(request, 'shop/cart.html', {
        'cart_products': s['cart'],
        'total_cart_quantity': s['total_cart_quantity'],
        'total_cart_sum': s['total_cart_sum'],
    })


def create_order(request):
    s = request.session
    if request.method == 'POST':
        form = OrderForm(request.POST)
        delivery_form = DeliveryForm(request.POST)
        if form.is_valid() and delivery_form.is_valid():
            this_form = form.save(commit=False)
            this_form.sum = s['total_cart_sum']
            this_form.save()
            order_num = this_form.pk
            this_delivery_form = delivery_form.save(commit=False)
            this_delivery_form.order_number = Order.objects.get(pk=order_num)
            this_delivery_form.delivery_service = request.POST.get(
                'delivery_service')
            this_delivery_form.save()
            payment = Payment.objects.create(
                order_number=Order.objects.get(pk=order_num),
                pay_method=request.POST.get('payment_method')
            )
            payment.save()
            list_for_mail = []
            for key, value in s['cart'].items():
                ord_prod = OrderedProduct.objects.create(
                    product_id=Product.objects.get(pk=int(key)),
                    order_number=Order.objects.get(pk=order_num),
                    name=value['title'],
                    price=value['price'],
                    quantity=value['product_quantity'],
                    sum=value['cost']
                )
                list_for_mail.append({
                    'title': value['title'],
                    'price': value['price'],
                    'quantity': value['product_quantity'],
                    'cost': value['cost'],
                })
                ord_prod.save()
            del s['cart']
            del s['total_cart_quantity']
            del s['total_cart_sum']
            # send_order_email(this_form.email, list_for_mail)
            # telbot_send_msg("Новый заказ!\nНомер заказа: {}\nE-mail: {}\nТелефон: {}".format(
            #     this_form.pk, this_form.email, this_form.phone))
            return HttpResponseRedirect(reverse('shop:thanks', kwargs={'order_num': order_num}))
        return HttpResponse('Some problems during form processing.')
    else:
        order_form = OrderForm()
        delivery_form = DeliveryForm()
        del_services = DeliveryService.objects.all()
        pay_methods = PaymentMethod.objects.all()
        ordered_products = s['cart']
        total_quant = s['total_cart_quantity']
        total_sum = s['total_cart_sum']
    return render(request, 'shop/order.html', {
        'order_form': order_form,
        'delivery_form': delivery_form,
        'del_services': del_services,
        'pay_methods': pay_methods,
        'ordered_products': ordered_products,
        'total_quant': total_quant,
        'total_sum': total_sum,
    })


def thanks(request, order_num):
    return render(request, 'shop/thanks.html', {
        'order_num': order_num,
    })


def choose_delivery(request):
    service_slug = request.GET.get('service_slug')
    service = DeliveryService.objects.get(slug=service_slug)
    delivery_form = DeliveryForm(auto_id=f'{service_slug}_id_%s')
    return render(request, 'shop/delivery.html', {
        'service': service,
        'delivery_form': delivery_form,
    })


def product_search(request):
    search_value = request.GET.get('data')
    search_res = Product.objects.filter(title__icontains=search_value)[:5]
    return render(request, 'shop/product_search.html', {
        'search_res': search_res,
        'search_value': search_value,
    })


def product_search_autocomplete(request):
    search_value = request.GET.get('data')
    data = Product.objects.filter(title__icontains=search_value)[:5]
    d1 = [i.title for i in data]
    d2 = {'data': d1}
    return JsonResponse(d2)
