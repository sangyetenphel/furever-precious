from django.forms import ModelForm
from .models import Review, Order

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'review', 'rating']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ['user', 'code', 'date_added', 'status', 'admin_note']