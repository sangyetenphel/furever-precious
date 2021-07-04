from django.forms import ModelForm, fields
from .models import Review, Cart, Order

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'review', 'rating']


class CartForm(ModelForm):
    class Meta:
        model = Cart    
        fields = ['variant', 'quantity']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        # fields = ['full_name', 'street_address', 'apt_number', 'city', 'state', 'zip_code', 'country', 'phone']
        exclude = ['user', 'code', 'date_added', 'status', 'admin_note']