from django.urls import path
from django.urls import path
from . import views
# from .views import ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('', views.home, name='store-home'),
    # path('review/<int:pk>', ReviewDetailView.as_view(), name='review-product'),
    # path('review/<int:product_id>/new', ReviewCreateView.as_view(), name='review-new'),
    # path('review/<int:pk>/update', ReviewUpdateView.as_view(), name='review-update'),
    # path('review/<int:pk>/delete', ReviewDeleteView.as_view(), name='review-delete'),
    path('products', views.products, name='products'),
    path('product/<int:id>', views.product, name='product'),
    path('review_product/<int:id>', views.review_product, name="review_product"),
    path('cart', views.cart, name='cart'),
    path('add_cart/<int:id>', views.add_cart, name='add_cart'),
    path('delete_cart/<int:id>', views.delete_cart, name='delete_cart'),
    # path('order', views.order, name='order'),
    path('ajax_sizes', views.ajax_sizes, name='ajax_sizes'),
    path('stripe_config/', views.stripe_config, name='stripe_config'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.SuccessView.as_view()),
    path('webhook', views.stripe_webhook),
]

