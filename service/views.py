from django.shortcuts import render
from django.core.paginator import Paginator

from accounts.models import UserProfile
from about.models import Testimonials
from shop.models import Product


# Create your views here.
def service(request):

    products = Product.objects.all().filter(is_available=True).order_by('id')

    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)

    testimonials = Testimonials.objects.filter(
        is_active=True
    )


    # For testimonials section
    testimonial_per_user = []

    for testimonial in testimonials:
        try:
            profile = UserProfile.objects.get(user=testimonial.user)
            testimonial_per_user.append({
                'testimonial': testimonial,
                'profile':  profile
            })
        except UserProfile.DoesNotExist:
            testimonial_per_user.append({
                'testimonial': testimonial,
                'profile': profile
            })

    context = {
        'products': page_products,
        "testimonials": testimonial_per_user,
    }

    return render(request, 'service/service.html', context)
