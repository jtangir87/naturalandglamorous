from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from products.models import Product, ProductCategory
from .forms import (
    AddToCartForm,
)
from django.forms import formset_factory
from cart.cart import Cart
# from orders.models import Order, OrderItem
from django.db.models import Sum
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib import messages
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import JsonResponse
import uuid
import stripe

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
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect("/shop/cart")


def update_cart_item(request):
    product_id = request.POST["product_id"]
    quantity = request.POST["quantity"]
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.update(product, quantity, product.price)

    return redirect("/shop/cart")


def get_cart(request):
    cart = Cart(request)
    cart_total = round(cart.summary(), 2)
    context = {
        "cart": cart,
        "key": settings.STRIPE_PUBLISHABLE_KEY,
        "total": cart_total,
    }

    return render(request, "shop/cart.html", context)


# ##DELIVERY VIEW ###
# def checkout(request):
#     cart = Cart(request)
#     if request.user.is_authenticated:
#         user = request.user
#         form = DeliveryCheckoutForm(
#             initial={
#                 "name": user.get_full_name(),
#                 "email": user.email,
#                 "phone": user.phone_number,
#                 "street_1": user.street_1,
#                 "city": user.city,
#                 "state": user.state,
#                 "zip": user.zip,
#             }
#         )
#     else:
#         form = DeliveryCheckoutForm()
#     if cart.summary() > float(request.tenant.profile.free_delivery_dollar_amount):
#         delivery_fee = 0
#     else:
#         delivery_fee = request.tenant.profile.delivery_fee
#     tax_amount = float(
#         round(
#             (cart.summary() + float(delivery_fee))
#             * (float(request.tenant.profile.sales_tax) / 100),
#             2,
#         )
#     )
#     cart_total = round(tax_amount + float(delivery_fee) + cart.summary(), 2) + float(
#         request.tenant.profile.service_fee
#     )
#     context = {
#         "cart": cart,
#         "key": settings.STRIPE_PUBLISHABLE_KEY,
#         "form": form,
#         "delivery_fee": delivery_fee,
#         "tax": tax_amount,
#         "total": cart_total,
#     }

#     return render(request, "checkout_delivery.html", context)


# def delivery_charge(request):
#     cart = Cart(request)
#     if cart.summary() > float(request.tenant.profile.free_delivery_dollar_amount):
#         delivery_fee = 0
#     else:
#         delivery_fee = request.tenant.profile.delivery_fee
#     tax_amount = float(
#         round(
#             (cart.summary() + float(delivery_fee))
#             * (float(request.tenant.profile.sales_tax) / 100),
#             2,
#         )
#     )
#     cart_total = round(tax_amount + float(delivery_fee) + cart.summary(), 2) + float(
#         request.tenant.profile.service_fee
#     )
#     if request.method == "POST":
#         form = DeliveryCheckoutForm(request.POST or None)
#         if form.is_valid():
#             customer = get_or_create_customer(
#                 form.cleaned_data["email"], request.POST["stripeToken"],
#             )
#             transfer_group = uuid.uuid4()
#             if request.tenant.profile.refund_fees > 0:
#                 ctg_fee = (
#                     round(float(request.tenant.profile.service_fee)
#                           * 0.971, 2) * 100
#                 ) + request.tenant.profile.refund_fees
#                 profile = Profile.objects.filter(tenant=request.tenant).first()
#                 profile.refund_fees = 0
#                 profile.save()
#             else:
#                 ctg_fee = (
#                     round(float(request.tenant.profile.service_fee)
#                           * 0.971, 2) * 100
#                 )
#             charge = stripe.Charge.create(
#                 amount=int(cart_total * 100),
#                 currency="usd",
#                 customer=customer.id,
#                 description="Cater To Go Order",
#                 destination={
#                     "amount": int((((cart_total * 100) * 0.971) - 30) - ctg_fee),
#                     "account": request.tenant.profile.stripe_user_id,
#                 },
#                 transfer_group=transfer_group,
#             )
#             if request.tenant.profile.sales_rep:
#                 try:
#                     salesrep = SalesRep.objects.filter(
#                         id=request.tenant.profile.sales_rep.id
#                     ).first()
#                     transfer = stripe.Transfer.create(
#                         amount=salesrep.commission,
#                         currency="usd",
#                         destination=salesrep.stripe_user_id,
#                         transfer_group=transfer_group,
#                     )
#                     print("commission PAID")
#                 except:
#                     print("Not able to transfer commission")
#             ## SEND EMAIL AND CLEAR CART ##
#             if charge.status == "succeeded":

#                 order_type = "Delivery"
#                 name = form.cleaned_data["name"]
#                 email = form.cleaned_data["email"]
#                 phone = form.cleaned_data["phone"]
#                 street_1 = form.cleaned_data["street_1"]
#                 city = form.cleaned_data["city"]
#                 state = form.cleaned_data["state"]
#                 zip = form.cleaned_data["zip"]
#                 pd_date = form.cleaned_data["pd_date"]
#                 notes = form.cleaned_data["notes"]

#                 ## CREATE SYSTEM ORDER ##
#                 created = timezone.now()
#                 if request.user.is_authenticated:
#                     order = Order.objects.create(
#                         customer=request.user,
#                         type=order_type,
#                         pd_date=pd_date,
#                         created=created,
#                         delivery_fee=delivery_fee,
#                         notes=notes,
#                         tax_collected=tax_amount,
#                         total=cart_total,
#                     )
#                 else:
#                     order = Order.objects.create(
#                         type=order_type,
#                         guest_name=name,
#                         guest_email=email,
#                         guest_phone=phone,
#                         guest_street_1=street_1,
#                         guest_city=city,
#                         guest_state=state,
#                         guest_zip=zip,
#                         pd_date=pd_date,
#                         created=created,
#                         notes=notes,
#                         delivery_fee=delivery_fee,
#                         tax_collected=tax_amount,
#                         total=cart_total,
#                     )

#                 order.save()
#                 for item in cart:
#                     OrderItem.objects.create(
#                         order=order,
#                         product=item.product,
#                         quantity=item.quantity,
#                         selections=item.selections,
#                         unit_price=item.unit_price,
#                         total_price=item.quantity * item.unit_price,
#                     )

#                 context = {
#                     "cart": cart,
#                     "order_type": order_type,
#                     "delivery_fee": delivery_fee,
#                     "name": name,
#                     "email": email,
#                     "phone": phone,
#                     "street_1": street_1,
#                     "city": city,
#                     "state": state,
#                     "zip": zip,
#                     "notes": notes,
#                     "pd_date": pd_date,
#                     "order_total": cart_total,
#                     "service_fee": request.tenant.profile.service_fee,
#                     "sales_tax_amount": tax_amount,
#                     "sales_tax": request.tenant.profile.sales_tax,
#                     "vendor": request.tenant.name,
#                     "vendor_email": request.tenant.profile.email,
#                     "vendor_phone": request.tenant.profile.phone,
#                 }
#                 ## EMAIL CUSTOMER ###
#                 txt_template = get_template("email/order_receipt.txt")
#                 html_template = get_template("email/order_receipt.html")
#                 text_content = txt_template.render(context)
#                 html_content = html_template.render(context)
#                 from_email = (
#                     "Cater To Go Orders" + "<" + request.tenant.profile.email + ">"
#                 )
#                 subject, from_email, to = (
#                     "Your Order Has Been Placed",
#                     from_email,
#                     email,
#                 )
#                 email = EmailMultiAlternatives(
#                     subject, text_content, from_email, [to])
#                 email.attach_alternative(html_content, "text/html")
#                 email.send()

#                 ## EMAIL VENDOR ###
#                 txt_template = get_template("email/vendor_new_order.txt")
#                 html_template = get_template("email/vendor_new_order.html")
#                 text_content = txt_template.render(context)
#                 html_content = html_template.render(context)
#                 from_email = "Cater To Go Orders <noreply@catertogo.com>"
#                 subject, from_email, to = (
#                     "NEW ORDER FROM CATER TO GO",
#                     from_email,
#                     request.tenant.profile.email,
#                 )
#                 email = EmailMultiAlternatives(
#                     subject, text_content, from_email, [to])
#                 email.attach_alternative(html_content, "text/html")
#                 email.send()

#                 ## CLEAR CART ##
#                 cart.clear()

#                 return render(request, "payment_successful.html")
#         else:
#             errors = form.errors
#             cart = Cart(request)
#             form = DeliveryCheckoutForm(request.POST)
#             context = {
#                 "cart": cart,
#                 "key": settings.STRIPE_PUBLISHABLE_KEY,
#                 "form": form,
#                 "errors": errors,
#                 "delivery_fee": delivery_fee,
#                 "tax": tax_amount,
#                 "total": cart_total,
#             }
#             return render(request, "checkout_delivery.html", context)


# def get_or_create_customer(email, token):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     connected_customers = stripe.Customer.list()
#     for customer in connected_customers:
#         if customer.email == email:
#             print(f"{email} found")
#             return customer
#     print(f"{email} created")
#     return stripe.Customer.create(email=email, source=token,)
