from django.shortcuts import render
from django.views.generic import DetailView


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


class ProductDetail(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = 'slug'
