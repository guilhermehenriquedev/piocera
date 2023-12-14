from competition.models import Edition
from django.shortcuts import render, get_object_or_404
from image_bank.models import Album, SubAlbum, Photos


def galeria(request):
    # Listando todos os albuns
    edition = Edition.objects.filter(status=3).latest('ano')
    subalbuns = SubAlbum.objects.all()
    albuns = SubAlbum.objects.all()
    return render(request, 'pages/albuns.html', locals())


def galeria_edicao(request, edicao_id):
    single_edition = get_object_or_404(Edition, id=edicao_id)
    edition = get_object_or_404(Edition, id=edicao_id)
    albuns = Album.objects.filter(edition=single_edition)
    subalbuns = SubAlbum.objects.filter(album__in=albuns)
    return render(request, 'pages/albuns.html', locals())


def sub_album_photos(request, edicao_id, subalbum_id):
    photos = Photos.objects.filter(subalbum=subalbum_id, subalbum__album__edition=edicao_id)
    num_photos = len(photos)
    num_columns = 4
    photos_per_column = num_photos // num_columns
    remaining_photos = num_photos % num_columns
    album_name = photos[0].subalbum.name
    edicao_id = photos[0].subalbum.album.edition.id

    columns = [[] for _ in range(num_columns)]
    photo_index = 0

    for i in range(num_columns):
        column_size = photos_per_column
        if i < remaining_photos:
            column_size += 1

        for _ in range(column_size):
            columns[i].append(photos[photo_index])
            photo_index += 1

    return render(request, 'pages/single_album.html', locals())
