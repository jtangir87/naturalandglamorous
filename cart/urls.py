"""cart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from .views import add_to_cart, get_cart, remove_from_cart, update_cart_item, checkout

from django.views.generic import TemplateView

app_name = "cart"

urlpatterns = [
    path('add-to-cart', add_to_cart, name="add_to_cart"),
    path('', get_cart, name="get_cart"),
    path("update", update_cart_item, name="update_cart_item"),
    path("<int:product_id>/remove", remove_from_cart, name="remove_from_cart"),
    path("checkout", checkout, name="checkout"),
    path("thanks", TemplateView.as_view(
        template_name="shop/thank_you.html"), name="thanks"),
]
