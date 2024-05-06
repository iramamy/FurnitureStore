from django.shortcuts import render, redirect
from django.contrib import messages
from .form import RegistrationForm
from .models import Account


# Create your views here.
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=username
            )

            user.phone_number = phone_number
            user.save()
            messages.success(request, "Registration successful!")

            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)


def signin(request):
    return render(request, 'accounts/signin.html')


def signout(request):
    return render(request, 'accounts/signout.html')
