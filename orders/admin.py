from django.contrib import admin
from .models import Order, OrderProduct, Payment

# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct

    readonly_fields = [
        'product',
        'payment',
        'quantity',
        'product_price',
        'total_amount',
        'ordered',
        'user',
    ]

    extra = 0


class OrderAdmin(admin.ModelAdmin):

    list_display_links = [
        'order_number',
        'full_name',
    ]

    list_display = (
        'order_number',
        'full_name',
        'is_ordered',
        'payment',
        'user',
        'status',
        'updated_at',
        
    )

    readonly_fields = [
        'first_name',
        'last_name',
        'user',
        'order_number',  
        'payment',
        'order_total',
        'tax',
        'is_ordered',
    ]

    list_filter = [
        'status',
        'payment',
        'is_ordered',
    ]

    list_per_page = 20

    inlines = [OrderProductInline]

class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = [
        'user',
        'payment_id',
        'payment_method',
        'amount_paid',
        'status',
    ]

    list_display = (
        'payment_id',
        'payment_method',
        'amount_paid',
        'status',
        'created_at',
        'user',
    )


class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        'payment',
        'product',
        'quantity',
        'product_price',
        'total_amount',
        'user',
        'updated_at',
    )

    readonly_fields = [
        'payment',
        'quantity',
        'product_price',
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Payment, PaymentAdmin)