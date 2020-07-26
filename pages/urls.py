from django.urls import path
from .views import home, contact_us

urlpatterns = [
    path('', home, name="home"),
    path('contact-us', contact_us, name="contact_us"),
]
