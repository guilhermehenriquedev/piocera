from .api.viewset import CompetitorCheckListViewSets, CompetitorCheckListRetrieveOrCreateViewSets, \
    addCheckListItemToCompetitorCheckList, removeCheckListItemFromCompetitor, createCompetitorCheckListItem
from .views import modality, category, inscricao_competicao, \
    register_pilot, buscar_cpf, payment_type, area_competidor, \
    registrar_documento_inscricao, inicio_area_competidor, \
    get_vehicle_models, editar_conta, lista_competidores, payment_pagseguro, competitor_boletos
from django.urls import path, include
from rest_framework import routers

route = routers.DefaultRouter()
route.register(r'competitor-check-list', CompetitorCheckListViewSets, basename='competitor_check_list')

urlpatterns = [
    path('', include(route.urls), name="api-competitor-check_list"),
    path('competitor-check_list/retrieveOrCreate/<int:competitor_registration>/<int:edition_id>',
         CompetitorCheckListRetrieveOrCreateViewSets.as_view(), name='area_competidor'),

    path('competitor-checklist/<int:competitor_checklist_id>/add-checklist-item/<int:checklist_item_id>/',
         addCheckListItemToCompetitorCheckList, name='add_checklist_item'),
    path('competitor-checklist/<int:competitor_checklist_id>/remove-checklist-item/<int:checklist_item_id>/',
         removeCheckListItemFromCompetitor, name='remove_checklist_item'),

    path('competitor-checklistitem/<int:competitor_checklist_id>/<int:checklist_item_id>/',
         createCompetitorCheckListItem, name='create_competitor_check_list_item'),

    path('<int:ano>/escolha-modalidade/', modality, name='modality'),
    path('<int:ano>/<slug:slug_modalidade>/escolher-categoria/', category,
         name='category'),
    path('<int:ano>/<slug:slug_modalidade>/<slug:slug_categoria>/<slug:lot_slug>/',
         inscricao_competicao, name='inscricao_competicao'),
    path('<int:ano>/<slug:slug_modalidade>/<slug:slug_categoria>/<slug:lot_slug>/inscricao-n.<int:inscricao>/',
         register_pilot, name='register_pilot'),
    path('buscar-cpf/', buscar_cpf, name='buscar_cpf'),
    path('get_vehicle_models/<int:brand_id>/', get_vehicle_models, name='get_vehicle_models'),
    path(
        '<int:ano>/<slug:slug_modalidade>/<slug:slug_categoria>/<slug:lot_slug>/inscricao-n.<int:inscricao>/pagamento/',
        payment_type, name='payment_type'),

    path('pagamento/pagseguro/inscricao-n.<int:inscricao>/<slug:lot_slug>/',
         payment_pagseguro, name='payment_pagseguro'),

    path('area-competidor/inscricao-n.<int:registration_id>/inscricao-competidor-n.<int:competitor_registration_id>/',
         area_competidor,
         name='area-competidor'),
    path('competidor-boletos/',
         competitor_boletos,
         name='competitor_boletos'),

    path(
        'registrar-documento-da-inscrição/inscricao-n.<int:competitor_registration_id>/documento/<int:document_type_id>/',
        registrar_documento_inscricao,
        name='registrar-documento-da-inscrição'),
    path('competitor_area/', inicio_area_competidor,
         name='competitor_area.html'),
    path('minha-conta/editar/', editar_conta, name='editar_conta'),
    path('lista-competidores/',
         lista_competidores, name='lista-competidores'),
]
