from django.shortcuts import render
from shop.models import Product
from django.core.paginator import Paginator

def home(request):

    """
        Return 3 products in home page.
    """
    
    products = Product.objects.all().filter(is_available=True).order_by('id') # noqa

    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)

    context = {
        'products': page_products,
    }

    return render(request, 'home.html', context)
