from django.db import models
from django.db.models import Avg
from django.db.models.deletion import SET_NULL
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from PIL import Image
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
    price = models.DecimalField(max_digits=6, decimal_places=2)
    keyword = models.CharField(max_length=255)
    date_added = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='products')
    description = RichTextUploadingField()
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    # amount = models.IntegerField()
    # min_amount = models.IntegerField()
    # status = models.BooleanField()

    def  __str__(self):
        return self.name

    def save(self):
        super().save()
         
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def image_tag(self):
        # mark_safe as an html for output in the admin page
        return mark_safe(f'<img src="{self.image.url}" height="50">')

    image_tag.short_description = "Product Image"

    def review_average(self):
        rating_dic = Review.objects.filter(product=self).aggregate(average_rating=Avg('rating'))
        rating = rating_dic['average_rating']
        if rating:
            rating_list = []
            for i in range(1, 6):
                if rating > i:
                    rating_list.append("fas fa-star")
                elif rating >= (i - 0.5):
                    rating_list.append('fas fa-star-half-alt')
                else:
                    rating_list.append('far fa-star')

            return rating_list
        else:
            return None

    def review_count(self):
        return Review.objects.filter(product=self).count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to="products")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Product images"

# class VariantManager(models.Manager):
#     def sizes(self):
#         return self.filter(category='size')


# PRODUCT_CATEGORIES = (
#     ('size', 'size'),
#     ('color', 'color'),
# )

class Color(models.Model):
    name = models.CharField(max_length=10)
    # color_code = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

    # def color_tag(self):
    #     if self.color_code:
    #         return mark_safe(f'<p style="background-color: {self.color_code}"></p>')


class Size(models.Model):
    name = models.CharField(max_length=3)
    
    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    title = models.CharField(max_length=250)
    # category = models.CharField(max_length=50, choices=PRODUCT_CATEGORIES, default='size')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

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



    # objects = VariantManager()

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, blank=True)
    review = models.TextField(blank=True)
    rating = models.IntegerField()
    date_added = models.DateTimeField(auto_now=True)

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
    variant = models.ForeignKey(ProductVariant, on_delete=SET_NULL, blank=True, null=True)
    quantity = models.IntegerField() 

    def __str__(self):
        return self.product.name

    @property
    def price(self):
        return self.product.price

    @property
    def amount(self):
        return self.quantity * self.product.price


class Order(models.Model):
    ORDER_STATUS = [
        # (db, front-end)
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('On Shipping', 'On Shipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Unique Order code to reference later, won't be displayed in admin/form
    code = models.CharField(max_length=5, editable=False)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    street_address = models.CharField(max_length=150, blank=True)
    apt_number = models.CharField(max_length=20)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=10) 
    country = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=ORDER_STATUS, default='New')
    admin_note = models.CharField(blank=True, max_length=100)


class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)








