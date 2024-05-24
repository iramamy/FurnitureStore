
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name='register'),
    path("signin/", views.signin, name='signin'),
    path("signout/", views.signout, name='signout'),

    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
    path("dashboard/", views.dashboard, name='dashboard'),

    # Forgot password
    path("forgotpassword/", views.forgotpassword, name='forgotpassword'),
    path(
        "reset_password_validate/<uidb64>/<token>/",
        views.reset_password_validate,
        name="reset_password_validate",
    ),

    # Reset password
    path("reset_password/", views.reset_password, name='reset_password'),

    # user dashboard
    path("my_orders/", views.my_orders, name='my_orders'),
    path("edit_profile/", views.edit_profile, name='edit_profile'),
    path("changepassword/", views.changepassword, name='changepassword'),

]
