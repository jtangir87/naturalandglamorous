from django.shortcuts import render
from django.views.generic import TemplateView
from blog.models import VlogPost

# Create your views here.


def home(request):
    rec_vlogs = VlogPost.objects.filter(
        published=True).order_by('-created_at')
    return render(request, 'pages/home.html', {'rec_vlogs': rec_vlogs})
