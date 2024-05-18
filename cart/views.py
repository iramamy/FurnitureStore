from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .models import Cart, CartItem


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart


@login_required(login_url= 'signin')
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # Get the product
    user = request.user

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart id in the session # noqa
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, user=user)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            user=user
        )
        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get the existing item
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity >= 2:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get the existing item
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()

    return redirect('cart')


@login_required(login_url='signin')
def cart(request, total=0, quantity=0, cart_items=None):
    tax, grand_total = 0, 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        shipping_handling = 10.0
        tax = (2 * total)/100
        grand_total = tax + total + shipping_handling

        context = {
        'total': total,
        "quantity": quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'shipping_handling': shipping_handling
        }

        return render(request, 'shop/cart.html', context)

    except ObjectDoesNotExist:
        pass


def checkout(request, total=0, quantity=0, cart_items=None):

    tax, grand_total = 0, 0
    try:
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        shipping_handling = 10.0
        tax = (2 * total)/100
        grand_total = tax + total + shipping_handling

        context = {
        'total': total,
        "quantity": quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'shipping_handling': shipping_handling
        }

        return render(request, "shop/checkout.html", context)

    except ObjectDoesNotExist:
        pass