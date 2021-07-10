from django.contrib import admin
from django.contrib.auth import models
from .models import Product, Review, ProductImage, Cart, OrderProduct, Order, ProductVariant, Color, Size
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('id',)
    extra = 5


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    readonly_fields = ('image_tag',)
    extra = 1
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag']
    readonly_fields = ('id', 'image_tag',)
    inlines = [ProductImageInline, ProductVariantInline]


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'product_variant', 'quantity', 'price', 'amount']


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('product', 'price', 'quantity', 'amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'address','address2', 'city', 'state', 'zip_code', 'country']
    inlines = [OrderProductInline]

    list_filter = ('status',)


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'quantity', 'amount']


admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(Review)
admin.site.register(ProductImage)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)


