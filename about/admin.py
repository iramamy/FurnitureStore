from django.contrib import admin
from .models import Testimonials


class TestimonialsAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'title',
        'is_active',
        'created_at',
    ]

    
    list_display_links = [
        'user',
        'title'
    ]

    readonly_fields = [
        'content'
    ]

admin.site.register(Testimonials, TestimonialsAdmin)