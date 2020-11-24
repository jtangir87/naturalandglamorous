from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from django.conf import settings
from products.models import Product, ProductCategory
from .forms import (
    CheckoutForm,
)
from django.forms import formset_factory
from cart.cart import Cart
# from orders.models import Order, OrderItem
from django.db.models import Sum
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import JsonResponse
import uuid
import stripe

stripe_pub_key = settings.STRIPE_PUBLISHABLE_KEY
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


# def add_to_cart(request):
#     product_id = request.POST["product_id"]
#     quantity = request.POST["quantity"]
#     product = Product.objects.filter(id=product_id).first()
#     cart = Cart(request)
#     cart.add(product, product.price, quantity)

#     context = {
#         "categories": Category.objects.all(),
#     }

#     messages.add_message(request, messages.SUCCESS, "Item Added To Cart")
#     return render(request, "home.html", context)


def add_to_cart(request):
    data = dict()
    if request.method == "POST":
        product_id = request.POST["product_id"]
        quantity = request.POST["quantity"]
        product = Product.objects.filter(id=product_id).first()
        cart = Cart(request)
        cart.add(product, product.price, quantity)
        data["form_is_valid"] = True
        return JsonResponse(data)


def remove_from_cart(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    cart = Cart(request)
    cart.remove(product)
    cart_total = round(cart.summary(), 2)
    context = {
        "cart": cart,
        "key": settings.STRIPE_PUBLISHABLE_KEY,
        "total": cart_total,
    }

    return render(request, "shop/cart.html", context)


def update_cart_item(request):
    product_id = request.POST["product_id"]
    quantity = request.POST["quantity"]
    product = Product.objects.filter(id=product_id).first()
    cart = Cart(request)
    cart.update(product, quantity, product.price)
    cart_total = round(cart.summary(), 2)
    context = {
        "cart": cart,
        "key": settings.STRIPE_PUBLISHABLE_KEY,
        "total": cart_total,
    }

    return render(request, "shop/cart.html", context)


def get_cart(request):
    cart = Cart(request)
    cart_total = round(cart.summary(), 2)
    context = {
        "cart": cart,
        "key": settings.STRIPE_PUBLISHABLE_KEY,
        "total": cart_total,
    }

    return render(request, "shop/cart.html", context)


##CHECKOUT VIEW ###
def checkout(request):
    cart = Cart(request)

    cart_total = round(cart.summary(), 2)

    if request.method == "POST":
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            try:
                customer = stripe.Customer.create(
                    email=form.cleaned_data["email"],
                    name=form.cleaned_data["name"],
                    source=request.POST["stripeToken"],
                )
            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught
                body = e.json_body
                err = body["error"]
                stripe_error = err["message"]

                context = {
                    "cart": cart,
                    "key": settings.STRIPE_PUBLISHABLE_KEY,
                    "form": CheckoutForm(request.POST),
                    "stripe_error": stripe_error,
                    "total": cart_total,
                }
                return render(request, "shop/checkout_form.html", context)

            stripe_amount = int(cart_total * 100)
            charge = stripe.Charge.create(
                customer=customer,
                amount=stripe_amount,
                currency="usd",
                description="N and G Order",
            )
            email_context = {
                "cart": cart,
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
                "street_1": form.cleaned_data["street_1"],
                "city": form.cleaned_data["city"],
                "state": form.cleaned_data["state"],
                "zip": form.cleaned_data["zip"],
                "amount": cart_total,
            }

            ## EMAIL VENDOR ##
            template = get_template("shop/emails/order_received.txt")

            content = template.render(email_context)
            send_mail(
                "New Order Received",
                content,
                "Website Orders <donotreply@elevatedwebsystems.com>",
                ["naturalandglamorous@gmail.com"],
                fail_silently=False,
            )

            # EMAIL CUSTOMER ##
            template = get_template("shop/emails/order_confirmation.txt")

            content = template.render(email_context)
            send_mail(
                "Thank You For Your Order",
                content,
                "Natural & Glamorous <naturalandglamorous@gmail.com>",
                [form.cleaned_data["email"]],
                fail_silently=False,
            )

            cart.clear()
            return HttpResponseRedirect("thanks")
        else:
            errors = form.errors
            context = {
                "cart": cart,
                "key": settings.STRIPE_PUBLISHABLE_KEY,
                "form": CheckoutForm(request.POST),
                "total": cart_total,
                "errors": errors,
            }
    else:

        context = {
            "cart": cart,
            "key": settings.STRIPE_PUBLISHABLE_KEY,
            "form": CheckoutForm(),
            "total": cart_total,
        }

    return render(request, "shop/checkout_form.html", context)
