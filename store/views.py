import json
from django.http import request 
import stripe

from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt 
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from .models import Order, OrderProduct, Product, ProductVariant, Review, Cart
from .forms import ReviewForm
from .utils import cart_items

# Create your views here.
def home(request):
    cart_items_total = cart_items(request)
    context = {
        'title': 'Home',
        'products': Product.objects.all(),
        'featured_products': Product.objects.filter(featured = True)[:4],
        'cart_items_total': cart_items_total
    }
    return render(request, 'store/home.html', context)


def about(request):
    cart_items_total = cart_items(request)
    context = {
        'cart_items_total': cart_items_total
    }
    return render(request, 'store/about.html', context)

def products(request):
    cart_items_total = cart_items(request)
    context = {
        'products': Product.objects.all(),
        'cart_items_total': cart_items_total
    }
    return render(request, 'store/products.html', context)


def product(request, id):
    cart_items_total = cart_items(request)
    product = Product.objects.get(pk=id)
    side_images = product.productimage_set.all()[:4]
    context = {
        'product': product,
        'reviews': Review.objects.filter(product=product).order_by('-date_added')[:2],
        'side_images': side_images,
        'cart_items_total': cart_items_total
    }
    if request.method == 'POST':
       pass
    else:
        variants = ProductVariant.objects.filter(product_id=id)
        if variants:
            sizes = [p.size for p in ProductVariant.objects.filter(product=product).order_by('size', 'date_added').distinct('size')]
            colors = ProductVariant.objects.filter(product=product, size=variants[0].size)
            variant = ProductVariant.objects.get(id=variants[0].id) 
            context.update({
                'sizes': sizes,
                'colors': colors,
                'variant': variant
            })   
    return render(request, 'store/product.html', context)


def ajax_sizes(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        product_id = body['productId']
        size_id = body['size']
        colors = ProductVariant.objects.filter(product_id=product_id, size_id=size_id)
        context = {
            'size_id': size_id,
            'product_id': product_id,
            'colors': colors
        }
        data = {
            'rendered_table': render_to_string('store/product_color_variants.html', context=context)
            }
        return JsonResponse(data)


def review_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = Review()
            new_review.subject = form.cleaned_data['subject']
            new_review.review = form.cleaned_data['review']
            new_review.rating = form.cleaned_data['rating']
            new_review.product = product
            new_review.reviewer = request.user
            new_review.save()
            messages.success(request, "Thank you for reviewing our product.")
            # Return back to the prev page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
        else:
            messages.error(request, "Error reviewing product. Try again!")
            return redirect('product', id=product.id)


# def get_productvariant(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         product_id = data['productId']
#         size_id = int(data['sizeId'])
#         color_id = data['colorId']
#         product_variant = ProductVariant.objects.filter(product_id=product_id, size_id=size_id, color_id=color_id)[0]
#         return JsonResponse(product_variant.id, safe=False)


def cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']
        size_id = int(data['sizeId'])
        color_id = data['colorId']
        quantity = data['quantity']
        product_variant = ProductVariant.objects.filter(product_id=product_id, size_id=size_id, color_id=color_id)[0]
        cart, created = Cart.objects.get_or_create(user=request.user, product_id=product_id, product_variant = product_variant)
        if created == True:
            cart.quantity = quantity
        else:
            cart.quantity += int(quantity)
        cart.save()
        return JsonResponse("Item quantity updated", safe=False)
    else:
        cart = Cart.objects.filter(user=request.user).order_by('date_added')
        cart_items_total = cart_items(request)
        sub_total = 0
        tax = 0
        for order in cart:
            sub_total += order.amount
        context = {
            'cart': cart,
            'sub_total': sub_total,
            'total': sub_total + tax,
            'cart_items_total': cart_items_total
        }
        return render(request, 'store/cart.html', context)


# @login_required
# def add_cart(request, id):
#     url = request.META.get('HTTP_REFERER')
#     product = Product.objects.get(id=id)
#     if request.method == 'POST':
#         if request.POST['variant']:
#             color_id = request.POST['color']
#             size_id = request.POST['size']
#             if size_id == 'None':
#                 size_id = None
#             variant = ProductVariant.objects.filter(product_id=id, size_id=size_id, color_id=color_id)[0]
#         else: 
#             variant = None
#         form = CartForm(request.POST)
#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']
#             # Check if the Product with the specific variant is already in Cart or not
#             if Cart.objects.filter(user=request.user, product_id=id, product_variant=variant):
#                 cart = Cart.objects.get(product_id=id)
#                 cart.quantity += quantity
#             else:
#                 cart = Cart()
#                 cart.user = request.user
#                 cart.product = product
#                 cart.product_variant = variant
#                 cart.quantity = quantity 
#             cart.save()
#             messages.success(request, "Your product has been added to cart!")
#         else:
#             print(form.errors)
#             return HttpResponse(form.errors)
            
#     return HttpResponseRedirect(url)


def delete_cart(request, id):
    Cart.objects.filter(id=id).delete()
    messages.success(request, "The item has been removed from your cart.")
    return redirect('cart')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    DOMAIN_URL = 'http://localhost:8000/'
    if request.method == 'POST':
        prev_url = request.META.get('HTTP_REFERER')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Creating line items to display the items from the current user's cart
        cart = Cart.objects.filter(user=request.user)
        line_items = []
        for item in cart:
            if item.product_variant:
                name = f"{item.product} {item.product_variant.color} {item.product_variant.size}"
                images = [item.product_variant.image()] 
            else:
                name = item.product.name
                images = [item.product.image.url]
        
            line_items_dic = {}
            line_items_dic['price_data'] = {
                'currency': 'usd',
                'unit_amount': int(item.price * 100),
                # 'tax_behavior': "exclusive",
                'product_data': {
                    'name': name,
                    'images': images,
                }
            }
            line_items_dic['quantity'] = item.quantity
            line_items.append(line_items_dic)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            shipping_address_collection = {
                'allowed_countries': ['US', 'CA'],
            },
            line_items = line_items,
            metadata = {
                'user_id': request.user.id,
            },
            # automatic_tax = {
            #     'enabled': True,
            # },
            mode='payment',
            success_url = DOMAIN_URL + 'success',
            cancel_url = prev_url,
        )
        return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Save an order in your database, marked as 'awaiting payment'
        create_order(session)

        # Check if the order is already paid (e.g., from a card payment)
        #
        # A delayed notification payment will have an `unpaid` status, as
        # you're still waiting for funds to be transferred from the customer's
        # account.
        if session.payment_status == "paid":
            # Fulfill the purchase
            fulfill_order(session)

    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']

        # Fulfill the purchase
        fulfill_order(session)

    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']

        # Send an email to the customer asking them to retry their order
        email_customer_about_failed_payment(session)

    # Passed signature verification
    return HttpResponse(status=200)


def create_order(session):
    user_id = session['metadata']['user_id']
    user = User.objects.get(id=user_id)
    order = Order()
    order.user = user
    order.email = session['customer_details']['email']
    order.name = session['shipping']['name']
    order.country = session['shipping']['address']['country']
    order.address = session['shipping']['address']['line1']
    order.address2 = session['shipping']['address']['line2']
    order.city = session['shipping']['address']['city']
    order.zip_code = session['shipping']['address']['postal_code']
    order.state = session['shipping']['address']['state']
    order.total = session['amount_total'] / 100
    order.status = 'Awaiting Payment'
    order.save()
    session['metadata']['order_id'] = order.id

    cart = Cart.objects.filter(user=user)
    for item in cart:
        order_product = OrderProduct()
        order_product.order = order
        order_product.product = item.product
        order_product.product_variant = item.product_variant
        order_product.quantity = item.quantity
        order_product.save()
    cart.delete()


def fulfill_order(session):
    order_id = session['metadata']['order_id']
    order = Order.objects.get(id = order_id)
    order.status = "Paid"
    order.save()


def success_order(request):
    cart_items_total = cart_items(request)
    return render(request, 'store/success.html', {'cart_items_total': cart_items_total})


def email_customer_about_failed_payment(session):
    pass
