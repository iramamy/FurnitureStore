from django.urls import path
from . import views

urlpatterns = [
    path("", views.about, name='about'),
    path("testimonial", views.testimonial, name='testimonial'),
]
