from django.urls import path

from .views import page

urlpatterns = [
    path('edicao/<int:ano>/<slug:slug>.html', page, name='flatpage_detail'),
]
