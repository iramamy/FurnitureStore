from django.shortcuts import render
from django.core.paginator import Paginator
from shop.models import Product

# Create your views here.
def service(request):

    products            = Product.objects.all().filter(is_available=True).order_by('id')

    paginator           = Paginator(products, 3)
    page_number         = request.GET.get('page')
    page_products       = paginator.get_page(page_number)

    context = {
        'products': page_products
    }

    return render(request, 'service/service.html', context)
