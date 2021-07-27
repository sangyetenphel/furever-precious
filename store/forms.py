from django.forms import ModelForm, fields
from .models import Review, Cart, Order

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'review', 'rating']


# class CartForm(ModelForm):
#     class Meta:
#         model = Cart    
#         fields = ['product_variant', 'quantity']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ['user', 'code', 'date_added', 'status', 'admin_note']