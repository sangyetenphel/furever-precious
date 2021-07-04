from django.contrib import admin
from django.contrib.auth import models
from .models import Product, Review, ProductImage, Cart, OrderProduct, Order, ProductVariant, Color, Size
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('id',)
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    readonly_fields = ('image_tag',)
    extra = 1
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag']
    readonly_fields = ('id', 'image_tag',)
    inlines = [ProductImageInline, ProductVariantInline]


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'price', 'amount']


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'price', 'quantity', 'amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'street_address', 'apt_number', 'city', 'state', 'zip_code', 'country' ]
    inlines = [OrderProductInline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'quantity', 'amount']
    list_filter = ['user']


admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(Review)
admin.site.register(ProductImage)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)


