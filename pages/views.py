from django.shortcuts import render
from django.views.generic import TemplateView
from blog.models import VlogPost

from django.template.loader import get_template
from django.http import JsonResponse
from django.core.mail import send_mail

# Create your views here.


def home(request):
    rec_vlogs = VlogPost.objects.filter(
        published=True).order_by('-created_at')
    return render(request, 'pages/home.html', {'rec_vlogs': rec_vlogs})


def contact_us(request):
    data = dict()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        template = get_template('pages/contact_us.txt')
        context = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        }
        content = template.render(context)
        send_mail(
            "N&G Contact Form",
            content,
            "{}<{}>".format(name, email),
            ['naturalandglamorous@gmail.com'],
            fail_silently=False,
        )
        data["form_is_valid"] = True
    else:
        data["form_is_valid"] = False
    return JsonResponse(data)
