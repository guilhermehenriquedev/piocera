from django.shortcuts import render, get_object_or_404

from flat_pages.models import Page


def page(request, ano, slug):
    postage = get_object_or_404(Page, slug=slug, edition__ano=ano)
    return render(request, 'pages/single_post.html', locals())
