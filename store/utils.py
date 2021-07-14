from .models import Cart

def cart_items(request):
    if  request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total = 0
        for items in cart:
            total += items.quantity
        return total
    else:
        return 0