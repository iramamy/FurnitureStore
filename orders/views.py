from django.shortcuts import render, redirect
import datetime

import json

from cart.models import CartItem
from .models import Order, Payment, OrderProduct
from .forms import OrderForm



# Create your views here.

def payments(request):

    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user,
        is_ordered=False,
        order_number=body['orderID']
    )

    # Store transaction details in payment
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        status=body['status'],
        amount_paid=order.order_total
    )

    payment.save()

    order.payment = payment
    order.is_ordered = True

    order.save()

    # Move cart item to OrderProduct db
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.payment = payment
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.total_price = item.quantity * item.product.price
        orderproduct.ordered = True

        orderproduct.save()

    # Decrease stock number

    # Clear cart

    # Email confirmation to user

    return render(request, 'orders/payments.html')

def place_order(request, total=0, quantity=0):

    current_user = request.user

    # If cart count is less or equal to 0 --> shop
    cart_item = CartItem.objects.filter(user=current_user)
    cart_count = cart_item.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for item in cart_item:
        total += (item.product.price * item.quantity)
        quantity += item.quantity

    tax = (2 * total)/100
    grand_total = total + tax


    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            # Store billing information to db
            data = Order()

            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.order_note = form.cleaned_data['order_note']

            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')

            data.save()

            # Create orderID
            yr = int(datetime.date.today().strftime("%Y"))
            mt = int(datetime.date.today().strftime("%m"))
            dt = int(datetime.date.today().strftime("%d"))

            d = datetime.date(yr, mt, dt)

            current_date = d.strftime("%Y%m%d")

            order_number = '#'+current_date + str(data.id)

            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, 
                is_ordered=False,
                order_number=order_number
                )

            context = {
                'order': order,
                'cart_item': cart_item,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,   
            }

            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


    return render(request, 'orders/place_order.html')
