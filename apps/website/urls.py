from django.urls import path
from .views import home, dashboard_admin, dashboard_admin_modalidades, dashboard_admin_category, update_history_payment, \
    aprove_document, recuse_document, exportar_xlsx, exportar_xlsx_modalidty, update_registration_category, \
    dashboard_admin_check_scanner, dashboard_admin_checkin, galeria_dos_compeoes, upload_documents, checkin_list, \
    newsletter_send_email, delete_registration_blank, atualizar_banners, pizza_chart, get_payment_data, \
    get_dados_periodo, download_ficha, update_registration_remake

urlpatterns = [
    # path('old', new_home, name='home_old'),
    path('', home, name='home'),
    path('newsletter_send_email', newsletter_send_email, name='newsletter_send_email'),
    path('delete_registration_blank', delete_registration_blank, name='delete_registration_blank'),
    path('atualizar_banners', atualizar_banners, name='atualizar_banners'),

    path('galeria-dos-campeoes', galeria_dos_compeoes, name='galeria-dos-compeoes'),
    path('cadastro_boleto', upload_documents, name='cadastro_boleto'),

    path('dashboard-admin/', dashboard_admin, name='dashboard-admin'),
    path('pizza_chart/', pizza_chart, name='pizza_chart'),
    path('get_payment_data/', get_payment_data, name='get_payment_data'),
    path('get_dados_periodo/', get_dados_periodo, name='get_dados_periodo'),
    path('download_ficha/<int:registration_id>', download_ficha, name='download_ficha'),


    path('dashboard-admin/checkin-list', checkin_list, name='checkin-list'),
    path('dashboard-admin/check-scanner', dashboard_admin_check_scanner, name='dashboard_admin_check_scanner'),
    path('dashboard-admin/checkin/<int:competitor_registration>/<int:edition_id>', dashboard_admin_checkin,
         name='dashboard_admin_checkin'),
    path('dashboard-admin/modalidades/', dashboard_admin_modalidades, name='dashboard_admin_modalidades'),
    path('dashboard-admin/modalidades/<str:modality_id>/', dashboard_admin_category, name='dashboard_admin_category'),
    path('dashboard-admin/modalidades/<str:payment_id>/<str:modality_id>/', update_history_payment, name='update_history_payment'),
    path('dashboard-admin/modalidades/registration/<str:payment_id>/<str:modality_id>/', update_registration_remake, name='update_registration_remake'),

    path('dashboard-admin/modalidades/category/<str:registration_id>/<str:modality_id>/', update_registration_category,
         name='update_registration_category'),

    path('aproved_document', aprove_document, name='aproved_document'),
    path('recuse_document/<str:doc_slug>/<str:user_id>/<str:registration_id>/', recuse_document,
         name='recuse_document'),

    path('exportar_csv', exportar_xlsx, name='exportar_csv'),
    path('exportar_csv_modalidty/<int:modality_edition_id>', exportar_xlsx_modalidty, name='exportar_csv_modalidty'),
]
