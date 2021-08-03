from django.urls import path
from django.urls import path
from . import views
# from .views import ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('', views.home, name='store-home'),
    path('about', views.about, name='about'),
    path('products', views.products, name='products'),
    path('product/<int:id>', views.product, name='product'),
    path('review_product/<int:id>', views.review_product, name="review_product"),
    path('cart', views.cart, name='cart'),
    path('add_cart', views.add_cart, name='add_cart'),
    path('delete_cart/<int:id>', views.delete_cart, name='delete_cart'),
    path('ajax_sizes', views.ajax_sizes, name='ajax_sizes'),
    path('stripe_config/', views.stripe_config, name='stripe_config'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.success_order, name='success-order'),
    path('webhook', views.stripe_webhook),
]

