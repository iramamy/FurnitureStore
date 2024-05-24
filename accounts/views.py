from django.shortcuts import render, redirect, get_object_or_404
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

from .form import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile

from orders.models import Order, OrderProduct


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

            # Create user profile
            user_profile = UserProfile()
            user_profile.user_id = user.id
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.phone_number = phone_number
            user_profile.profile_picture = 'default/default.png'
            user_profile.save()

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
    orders = Order.objects.order_by('-created_at').filter(
        user_id=request.user.id,
        is_ordered=True
    )

    userprofile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    order_count = orders.count()
    context = {
        'order_count': order_count,
        "userprofile": userprofile
    }

    return render(request, 'accounts/dashboard.html', context)

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


@login_required(login_url='signin')
def my_orders(request):
    
    orders = Order.objects.filter(
        user=request.user,
        is_ordered=True
    ).order_by('-created_at')

    order_exist = orders.exists()

    context = {
        'orders': orders,
        "order_exist": order_exist
    }

    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url='signin')
def edit_profile(request):

    userprofile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, 
            request.FILES,
            instance=userprofile
            )

        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()

            messages.success(request, "Your profile has been updated!")

            return redirect(edit_profile)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "userprofile": userprofile
    }

    return render(request, 'accounts/edit_profile.html', context )


@login_required(login_url='signin')
def changepassword(request):

    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(
            username__exact=request.user.username
            )

        if new_password == confirm_password:
            success = user.check_password(current_password)

            if success:
                user.set_password(new_password)
                user.save()

                messages.success(request, "Password updated successfuly!")

                return redirect("changepassword")

            else:
                messages.error(request, "Please enter valid credential!")
                return redirect("changepassword")
        
        else:
            messages.error(request, "Password does not match!")
            return redirect('changepassword')
        
    return render(request, 'accounts/changepassword.html')


@login_required(login_url='signin')
def order_detail(request, order_id):

    order_detail = OrderProduct.objects.filter(
        order__order_number=order_id
    )

    order = Order.objects.get(
        order_number=order_id
    )

    subtotal = 0
    shipping = 10.0
    tax = order.tax

    for i in order_detail:
        subtotal += i.product_price * i.quantity
    
    grand_total = subtotal + shipping + tax

    context = {
        "order_detail": order_detail,
        "order": order,
        "subtotal": subtotal,
        "grand_total": grand_total,
        'tax': tax,
        "shipping": shipping
    }

    return render(request, 'accounts/order_detail.html', context)