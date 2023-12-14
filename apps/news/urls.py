from django.urls import path

from .views import noticias, postage_detail
from django.urls import path

app_name = 'news'

urlpatterns = [
    path('', noticias, name='noticias'),
    #path('edicao/<int:ano>/<slug:slug>.html', postage_detail, name='postage_detail'),
    path('postage/<int:ano>/<slug:slug>/', postage_detail, name='postage_detail'),

]
