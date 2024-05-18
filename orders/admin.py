from django.contrib import admin
from .models import Order, OrdreProduct, Payment

# Register your models here.

class OrderAdmin(admin.ModelAdmin):

    list_display_links = [
        'order_number',
        'full_name',
    ]

    list_display = (
        'order_number',
        'full_name',
        'payment',
        'updated_at',
        'user',
        'status',
    )

    readonly_fields = [
        'order_number',  
        'payment',
        'order_total',
        'tax',
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrdreProduct)
admin.site.register(Payment)