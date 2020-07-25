from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Category, VlogPost

# Register your models here.


class VlogPostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'


admin.site.register(Category)
admin.site.register(VlogPost, VlogPostAdmin)
