from http.client import HTTPResponse

from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from competition.models import WebSiteEdition, Banner, Edition, Sponsor
from image_bank.models import Album, SubAlbum
from news.models import News
from radical.utils.utils import define_logo
from website.models import WebSite, Questions

from datetime import datetime, timezone, timedelta


# Create your views here.
def all_editions(request):
    editions = Edition.objects.all()
    banners = {}
    for issue in editions:
        banners_ = Banner.objects.filter(edition=issue)
        banners_list = []
        for banner in banners_:
            banners_list.append(banner)
        banners[issue.ano] = banners_list
    return render(request, 'all-editions.html', locals())


def edition(request, ano):
    edition = get_object_or_404(Edition, ano=ano)
    news = News.news.filter(edition=edition)[:4]
    website_info = WebSite.objects.last()
    faqs = Questions.objects.filter(is_active=True)

    currentDateAndTime = datetime.now(timezone.utc)

    currentDate = currentDateAndTime
    editionDate = edition.edition_date

    diferenca = editionDate - currentDate
    dias = diferenca.days if diferenca.days > 0 else 0
    segundos = diferenca.seconds
    horas = segundos // 3600 if segundos // 3600 > 0 else 0
    minutos = (segundos % 3600) // 60 if (segundos % 3600) // 60 > 0 else 0
    segundos = (segundos % 60) if (segundos % 60) > 0 else 0

    try:
        previous_edition = WebSiteEdition.objects.get(edition=edition)
    except Exception as e:
        print(e)

    banners_ = Banner.objects.filter(edition=edition)
    banners = {}
    for banner in banners_:
        banners[banner.position] = banner
    banners_with_text = banners_.filter(position=3)
    sponsor = Sponsor.objects.filter(edition=edition)
    patrocinadores = sponsor.filter(type=1)
    co_patrocinadores = sponsor.filter(type=2)
    apoios = sponsor.filter(type=3)
    gallery = Album.objects.filter(edition=edition)
    albuns = SubAlbum.objects.filter(album__in=gallery)

    logos = define_logo(request, edition.type)

    return render(request, 'website/home.html', locals())
