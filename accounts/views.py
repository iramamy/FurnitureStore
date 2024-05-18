from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# User activation
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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

            # User activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string(
                "accounts/account_verification_email.html",
                {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })

            to_email = email
            send_email = EmailMessage(
                mail_subject,
                message,
                to=[to_email]
            )

            send_email.send()

            # messages.success(request, "Registration successful!")

            return redirect('/accounts/signin/?command=verify&email='+email) # noqa
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(
            email=email,
            password=password
        )

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in!")

            return redirect('dashboard')

        else:
            messages.error(request, "Invalid login credentials!")
            return redirect('signin')

    return render(request, 'accounts/signin.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token): # noqa
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations, your account is activated!") # noqa

        return redirect('signin')

    else:
        messages.error(request, "Invalid actication link!")

        return redirect('register')


@login_required(login_url='signin')
def signout(request):
    auth.logout(request)
    messages.success(request, "You are logged out!")

    return redirect('signin')


@login_required(login_url='signin')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def forgotpassword(request):

    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Please reset your password'
            message = render_to_string(
                "accounts/password_reset_email.html",
                {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })

            to_email = email
            send_email = EmailMessage(
                mail_subject,
                message,
                to=[to_email]
            )

            send_email.send()
            messages.success(request, "An email has been sent to reset your password!") # noqa

            return redirect('signin')

        else:
            messages.error(request, "Account does not exist!")
            return redirect('forgotpassword')

    return render(request, "accounts/forgotpassword.html")

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token): # noqa
        request.session['uid'] = uid
        messages.success(request, "Please reset your password!")

        return redirect('reset_password')
    else:
        messages.error(request, "This link as been expired!")

        return redirect('signin')

def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:

            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()

            messages.success(request, "Password reset successful!")
            return redirect("signin")

        else:
            messages.error(request, "This link has been expired!")

            return redirect("forgotpassword")

    return render(request, 'accounts/reset_password.html')
