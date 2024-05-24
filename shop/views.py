from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages

from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from .models import Product, ReviewRating
from .forms import ReviewForm

from orders.models import OrderProduct
from accounts.models import UserProfile


# Create your views here.
def shop(request, category_slug=None):

    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
                                category=categories,
                                is_available=True).order_by('id')
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        page_product = paginator.get_page(page)

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id') # noqa
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        page_product = paginator.get_page(page)

    # Get reviews

    for single_product in products:
        reviews = ReviewRating.objects.filter(
            product_id=single_product.id,
            status=True
        )

    context = {
        'products': page_product,
        'reviews': reviews
    }
    return render(request, 'shop/shop.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        # Single product
        single_product = Product.objects.get(
            category__slug=category_slug, 
            slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request),
            product=single_product
            ).exists()

    except Exception as e:
        raise e

    order_product = None
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(
                user=request.user,
                product_id=single_product.id
            ).exists()

        except OrderProduct.DoesNotExist:
            order_product = None

    # Get reviews
    reviews = ReviewRating.objects.filter(
        product_id=single_product.id,
        status=True
    )

    reviews_per_user = []
    for review in reviews:
        try:
            profile = UserProfile.objects.get(
                user=review.user
            )
            reviews_per_user.append({
                'review': review,
                'profile': profile
            })

        except UserProfile.DoesNotExist:
            reviews_per_user.append({
                'review': review,
                'profile': None
            })
    
    review_count = reviews.count()

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "order_product": order_product,
        "reviews": reviews_per_user,
        "review_count": review_count
    }

    return render(request, 'shop/product_detail.html', context)


def submitreview(request, product_id):

    url = request.META.get("HTTP_REFERER")

    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(
                user__id=request.user.id,
                product__id=product_id
            )
            form = ReviewForm(request.POST, instance=reviews) # update
            form.save()

            messages.success(request, "Your review has been updated")

            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)

            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get("REMOTE_ADDR")

                data.product_id = product_id
                data.user_id = request.user.id

                data.save()

                messages.success(request, "Thanks for your review")

                return redirect(url)
        
