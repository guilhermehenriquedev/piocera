from django.urls import path
from apps.image_bank.views import galeria, galeria_edicao,sub_album_photos

urlpatterns = [
    path('', galeria, name='galeria'),
    path('edicao/<int:edicao_id>', galeria_edicao, name='galeria_edicao'),
    path('edicao/<int:edicao_id>/subalbum/<int:subalbum_id>/fotos', sub_album_photos, name='sub_album_photos'),
]
