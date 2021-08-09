import json
from .models import Cart, Product, ProductVariant

def cart_items(request):
    cart_items_total = 0
    if  request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        for items in cart:
            cart_items_total += items.quantity
    else:
        try: 
            cookie_cart = json.loads(request.COOKIES['cart'])
        except:
            cookie_cart = {}
        for variants in cookie_cart.values():
            for variant in variants:
                cart_items_total += variant['quantity']
    return cart_items_total
        
        
def cookie_cart(request):
    try: 
        cookie_cart = json.loads(request.COOKIES['cart'])
    except:
        cookie_cart = {}
    cart_items_total = 0
    sub_total = 0
    cart = []
    for product, variants in cookie_cart.items():
        product = Product.objects.get(id=product)
        for variant in variants:
            if variant['sizeId'] == "None" or variant['sizeId'] == '':
                product_variant = ProductVariant.objects.filter(product=product, color_id = variant['colorId'])[0]
            else:
                product_variant = ProductVariant.objects.filter(product=product, size_id = variant['sizeId'], color_id = variant['colorId'])[0]
            cart_items_total += variant['quantity']
            if product_variant:
                amount = variant['quantity'] * product_variant.price
            else:
                amount = variant['quantity'] * product.price
            sub_total += amount
            cart.append({
                'product': product,
                'product_variant': product_variant,
                'quantity': variant['quantity'],
                'amount': amount
            })
    data = {
        'cart': cart,
        'sub_total': sub_total,
        'total': sub_total,
        'cart_items_total': cart_items_total
    }
    return data