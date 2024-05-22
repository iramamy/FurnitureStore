from django.db import models
from django.urls import reverse

from django.db.models import Avg, Count

from category.models import Category

from accounts.models import Account


# Create your models here.
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return str(self.product_name)

    def average_review(self):
        reviews = ReviewRating.objects.filter(
            product=self,
            status=True
        ).aggregate(average=Avg('rating'))

        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])

        return avg


    def review_count(self):
        reviews = ReviewRating.objects.filter(
            product=self,
            status=True
        ).aggregate(count=Count('id'))

        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])

        return count


class ReviewRating(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject