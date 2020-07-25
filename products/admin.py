from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import ProductCategory, Product

# Register your models here.


class ProductAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'


admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
