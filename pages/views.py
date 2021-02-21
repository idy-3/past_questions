from django.shortcuts import render, get_object_or_404

from pages.models import Content


def index(request):
    return render(request, 'pages/index.html')


def page(request, slug):
    content = get_object_or_404(Content, slug=slug)

    context = {'content': content}

    return render(request, 'pages/page.html', context)
