from django.shortcuts import render


def contact(request):
    return render(request, 'contact/contact_us.html')