
from django.urls import path
from . import views

urlpatterns = [
    path("", views.shop, name='shop'),

    # Category
    path("<slug:category_slug>/", views.shop, name='product_by_category'),
    # Product detail
    path(
        "<slug:category_slug>/<slug:product_slug>/", 
        views.product_detail, 
        name='product_detail'
        ),

    # Reviews
    path("submitreview/<int:product_id>", views.submitreview, name='submitreview'),
]
