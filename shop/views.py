from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from category.models import Category
from .models import Product


# Create your views here.
def shop(request, category_slug=None):

    categories              = None
    products                = None

    if category_slug is not None:
        categories          = get_object_or_404(Category, slug=category_slug)
        products            = Product.objects.filter(
                                category=categories, 
                                is_available=True).order_by('id')
        paginator           = Paginator(products, 8)
        page                = request.GET.get('page')
        page_product        = paginator.get_page(page)

    else:
        products            = Product.objects.all().filter(is_available=True).order_by('id')
        paginator           = Paginator(products, 8)
        page                = request.GET.get('page')
        page_product        = paginator.get_page(page)

    context = {
        'products': page_product,
    }
    return render(request, 'shop/shop.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        # Single product
        single_product      = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    context                 = {
        "single_product"        : single_product,
    }

    return render(request, 'shop/product_detail.html', context)
