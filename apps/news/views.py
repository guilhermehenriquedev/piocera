from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse
from .models import News


def noticias(request):
    news = News.news.get_queryset()
    context = {'news': news}
    # publication_date = news[0].publication_date
    # edition = news[0].edition
    return render(request, 'pages/news.html', context)


def postage_detail(request, ano, slug):
    try:
        postage = News.objects.filter(slug=slug, edition__ano=ano).get()
    except News.news.DoesNotExist:
        return HttpResponse("A notícia não existe.")

    return render(request, 'pages/single_news.html', locals())
