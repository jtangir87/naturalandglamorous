from django.shortcuts import render
from django.views.generic import ListView, TemplateView


from .models import Category, VlogPost
# Create your views here.


class VlogList(TemplateView):
    template_name = "blog/vlog_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vlogs"] = VlogPost.objects.filter(
            published=True)
        context["categories"] = Category.objects.all()
        return context


def filtered_vlog_list(request, slug):
    category = Category.objects.filter(slug=slug).first()

    vlogs = VlogPost.objects.filter(categories=category, published=True)

    context = {
        'categories': Category.objects.all(),
        'category': category,
        'vlogs': vlogs
    }

    return render(request, 'blog/vlog_list_filtered.html', context)


def vlog_detail(request, slug):
    vlog = VlogPost.objects.filter(slug=slug).first()

    context = {
        'categories': Category.objects.all(),
        'vlog': vlog
    }

    return render(request, 'blog/vlog_detail.html', context)
