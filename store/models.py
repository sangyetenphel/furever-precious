import math
from django.db import models
from django.db.models import Avg
from django.db.models.deletion import SET_NULL
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Product(models.Model):
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color')
    )
    
    name = models.CharField(max_length=255)
    SKU = models.CharField(max_length=10, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='products')
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)

    def  __str__(self):
        return self.name

    def image_tag(self):
        # mark_safe as an html for output in the admin page
        return mark_safe(f'<img src="{self.image.url}" height="50">')

    image_tag.short_description = "Product Image"

    def review_average(self):
        return Review.objects.filter(product=self).aggregate(average_rating=Avg('rating'))['average_rating']

    def review_average_stars(self):
        rating = Review.objects.filter(product=self).aggregate(average_rating=Avg('rating'))['average_rating']
        if not rating:
            return None
        stars = []
        after_decimal, before_decimal = math.modf(rating)
        for _ in range(int(before_decimal)):
            stars.append('fas fa-star')

        if after_decimal:
            stars.append('fas fa-star-half-alt')

        for _ in range(5 - math.ceil(rating)):
            stars.append('far fa-star')

        return stars

    def review_count(self):
        return Review.objects.filter(product=self).count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to="products")

    class Meta:
        verbose_name_plural = "Product images"

    def __str__(self):
        return self.product.name


class Color(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=5)
    
    def __str__(self):
        if self.name == None:
            return "One Size"
        return self.name
        

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory_quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.size:
            return f"{self.product.name} {self.size.code} {self.color}" 
        else:
            return f"{self.product.name} {self.color}" 

    def image(self):
        img_query_set = ProductImage.objects.filter(id=self.image_id) 
        if img_query_set:
            img = img_query_set[0].image.url
        else:
            img = ''
        return img

    def image_tag(self):
        img_query_set = ProductImage.objects.filter(id=self.image_id)
        if img_query_set:
            return mark_safe(f'<img src="{img_query_set[0].image.url}" height="50"')
        else:
            return ''


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=150, blank=True)
    review = models.TextField(blank=True)
    rating = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review

    def get_absolute_url(self):
        return reverse('review-product', kwargs={'pk': self.product.id})

    def rating_star(self):
        if self.rating:
            stars = []
            for i in range(5):
                if self.rating > i:
                    stars.append('fas fa-star')
                else:
                    stars.append('far fa-star')
            return stars
        else:
            return None


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1) 
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
        
    @property
    def price(self):
        if self.product_variant:
            return self.product_variant.price
        return self.product.price

    @property
    def amount(self):
        if self.product_variant:
            return self.quantity * self.product_variant.price
        return self.quantity * self.product.price
    

class Order(models.Model):
    ORDER_STATUS = [
        ('Awaiting Payment', 'Awaiting Payment'),
        ('Paid', 'Paid'),
        ('On Shipping', 'On Shipping'),
        ('Completed', 'Completed'),
        ('Payment Failed', 'Payment Failed'),
        ('Cancelled', 'Cancelled')
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # code = models.CharField(max_length=5, editable=False)
    email = models.EmailField(max_length=265)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=10) 
    state = models.CharField(max_length=150)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS)

    def __str__(self):
        return f"{self.address} {self.address2}, {self.city}, {self.state}, {self.country} {self.zip_code}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        if self.product_variant:
            return self.product_variant.__str__()
        return self.product

    @property
    def price(self):
        if self.product_variant:
            return self.product_variant.price
        return self.product.price

    @property
    def amount(self):
        if self.product_variant:
            return self.quantity * self.product_variant.price
        return self.quantity * self.product.price
    
    @property
    def image(self):
        if self.product_variant:
            return self.product_variant.image()
        return self.product.image.url









