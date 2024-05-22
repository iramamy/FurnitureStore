from django.contrib import admin
from .models import Product, ReviewRating

class ProductAdmin(admin.ModelAdmin):
    list_display           = [
        'product_name', 
        'category', 
        'price', 
        'stock', 
        'modified_date', 
        'is_available'
        ]

    prepopulated_fields     = {'slug': ('product_name',)}
    list_editable           = ('price', 'stock', 'is_available')

    list_filter             = ('category', 'is_available')


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = [
        'subject',
        'user',
        'product',
        'rating',
        'updated_date'
    ]

    list_display_links = [
        'subject',
        'user',
    ]

admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)

