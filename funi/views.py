from django.shortcuts import render
from shop.models import Product
from django.core.paginator import Paginator

def home(request):
    products            = Product.objects.all().filter(is_available=True).order_by('id')

    paginator           = Paginator(products, 3)
    page_number         = request.GET.get('page')
    page_products       = paginator.get_page(page_number)

    context = {
        'products': page_products
    }

    return render(request, 'home.html', context)
