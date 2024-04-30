from django.contrib import admin
from .models import Product

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

# Register your models here.
admin.site.register(Product, ProductAdmin)

