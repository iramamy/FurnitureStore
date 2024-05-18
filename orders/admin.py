from django.contrib import admin
from .models import Order, OrdreProduct, Payment

# Register your models here.

admin.site.register(Order)
admin.site.register(OrdreProduct)
admin.site.register(Payment)