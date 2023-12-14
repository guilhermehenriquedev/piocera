from django.urls import path
from apps.competition.views import all_editions, edition
from apps.competition.api.viewset import EditionViewSet, FederationViewSet, SponsorViewSet, BannerViewSet, \
    WebSiteEditionViewSet, CompetitionModalityViewSet, ModalityEditionViewSet, CompetitionCategoryViewSet, \
    CategoryModalityViewSet

urlpatterns = [
    path('', all_editions, name='all_editions'),
    path('<int:ano>', edition, name='edition'),
    # API
    path('api/edition/', EditionViewSet.as_view({'get': 'list', }), name='edition_api_list'),
    path('api/edition/<int:pk>', EditionViewSet.as_view({'get': 'retrieve'}), name='edition_api_retrieve'),
    path('api/federation/', FederationViewSet.as_view({'get': 'list', }), name='federation_api_list'),
    path('api/federation/<int:pk>', FederationViewSet.as_view({'get': 'retrieve'}), name='federation_api_retrieve'),
    path('api/sponsor/', SponsorViewSet.as_view({'get': 'list', }), name='sponsor_api_list'),
    path('api/sponsor/<int:pk>', SponsorViewSet.as_view({'get': 'retrieve'}), name='sponsor_api_retrieve'),
    path('api/banner/', BannerViewSet.as_view({'get': 'list', }), name='banner_api_list'),
    path('api/banner/<int:pk>', BannerViewSet.as_view({'get': 'retrieve'}), name='banner_api_retrieve'),
    path('api/web_site/', WebSiteEditionViewSet.as_view({'get': 'list', }), name='web_site_api_list'),
    path('api/web_site/<int:pk>', WebSiteEditionViewSet.as_view({'get': 'retrieve'}), name='web_site_api_retrieve'),
    path('api/competition_modality/', CompetitionModalityViewSet.as_view({'get': 'list', }),
         name='competition_modality_api_list'),
    path('api/competition_modality/<int:pk>', CompetitionModalityViewSet.as_view({'get': 'retrieve'}),
         name='competition_modality_api_retrieve'),
    path('api/modality_edition/', ModalityEditionViewSet.as_view({'get': 'list', }),
         name='modality_edition_api_list'),
    path('api/modality_edition/<int:pk>', ModalityEditionViewSet.as_view({'get': 'retrieve'}),
         name='modality_edition_api_retrieve'),
    path('api/competition_category/', CompetitionCategoryViewSet.as_view({'get': 'list', }),
         name='competition_category_api_list'),
    path('api/competition_category/<int:pk>', CompetitionCategoryViewSet.as_view({'get': 'retrieve'}),
         name='competition_category_api_retrieve'),
    path('api/category_modality/', CategoryModalityViewSet.as_view({'get': 'list', }),
         name='category_modality_api_list'),
    path('api/category_modality/<int:pk>', CategoryModalityViewSet.as_view({'get': 'retrieve'}),
         name='category_modality_api_retrieve'),
]
