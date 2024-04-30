from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator

# Create your views here.
def shop(request):
    products            = Product.objects.all().filter(is_available=True).order_by('id')
    paginator           = Paginator(products, 8)
    page                = request.GET.get('page')
    page_product        = paginator.get_page(page)

    context = {
        'products': page_product,
    }
    return render(request, 'shop/shop.html', context)
