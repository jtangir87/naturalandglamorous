from django.shortcuts import render
from .models import ProductCategory, Product

# Create your views here.


def shop_landing_page(request):
    products = Product.objects.filter(active=True)
    new_items = products.order_by('-created_at')[:5]
    context = {
        "categories": ProductCategory.objects.all(),
        "products": products,
        "new_items": new_items,
    }

    return render(request, "shop/shop_landing_page.html", context)
