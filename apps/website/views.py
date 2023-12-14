import json
import pprint
from operator import attrgetter
import io
import openpyxl
from django.db.models import OuterRef, Subquery
import threading
from openpyxl.writer.excel import save_workbook
from rest_framework.decorators import api_view
from django.db import connection
from django.http import JsonResponse, HttpResponse
from competition.models import WebSiteEdition, Banner, Edition, Sponsor, ModalityEdition, CategoryModality
from image_bank.models import Album, SubAlbum
from news.models import News
from competitor.models import CompetitorsRegistration
from competitor.models import Registration, RegistrationDocuments, Document

from competitor.models import CheckListItem, CheckList, CompetitorCheckList, Boleto, Team
from rest_framework import status
from rest_framework.response import Response

from radical.utils.utils import send_email_async
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.website.forms import AdminPaymentForm, AdminRecuseDocumentForm, RegistrationAdminForm, LotAdminForm, \
    ChampionEditionForm, NewsletterForm
from radical.utils.utils import define_logo
from website.models import WebSite, Questions, Champion, Newsletter
from django.shortcuts import render, redirect
from datetime import datetime, timezone, timedelta
from django.urls import reverse
from django.contrib.auth.views import PasswordResetView

from django.contrib.admin.views.decorators import staff_member_required
from users.models import User
from financial.models import Lot, Order, PaymentHistory, AccountBank, PAYMENT_FORM
from datetime import date
from django.db.models import Sum, Count, Q, Max

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import ExtractMonth

from django.db.models import Value
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.forms.utils import ErrorDict


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            pass

        return super().form_valid(form)


def home(request):
    edition = Edition.objects.latest('ano')

    news = News.news.order_by('-publication_date')[:6]
    website_info = WebSite.objects.last()
    faqs = Questions.objects.filter(is_active=True)

    current_date_and_time = datetime.now(timezone.utc)
    current_date_date = current_date_and_time.date()

    current_date = current_date_and_time
    edition_date = edition.edition_date

    edition_date_iso = edition_date.isoformat()

    difference = edition_date - current_date
    dias = difference.days if difference.days > 0 else 0
    segundos = difference.seconds
    horas = segundos // 3600 if segundos // 3600 > 0 else 0
    minutos = (segundos % 3600) // 60 if (segundos % 3600) // 60 > 0 else 0
    segundos = (segundos % 60) if (segundos % 60) > 0 else 0

    try:
        previous_edition = WebSiteEdition.objects.get(edition=edition)
    except Exception as e:
        print(e)

    banners_ = Banner.objects.filter(edition=edition)
    main_banner = Banner.objects.filter(edition=edition, position=1)
    main_banner = sorted(main_banner, key=attrgetter('order'))
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

    gallery = gallery[:4]  # limit
    albuns = albuns[:4]  # limit
    modalities = ModalityEdition.objects.filter(edition=edition).order_by('position')
    news_form = NewsletterForm()
    return render(request, 'pages/home.html', locals())


@staff_member_required
def dashboard_admin_modalidades(request):
    editions = Edition.objects.all()

    if request.GET.get('edition_ano') and request.GET.get('edition_type'):
        edition_ano = request.GET.get('edition_ano')
        edition_type = request.GET.get('edition_type')
        modalities = ModalityEdition.objects.filter(edition__ano=edition_ano, edition__type=edition_type).order_by(
            'position')
    else:
        modalities = ModalityEdition.objects.all().order_by('position')

    for MODALITY in modalities:
        MODALITY.competitors_count = CompetitorsRegistration.objects.filter(
            registration__lot__category_modality__modality_edition=MODALITY
        ).count()
        MODALITY.registrations_count = Registration.objects.filter(
            lot__category_modality__modality_edition=MODALITY,
            status='3'
        ).count()
        MODALITY.category_name = CategoryModality.objects.filter(modality_edition__modality=MODALITY.modality,
                                                                 modality_edition__edition__ano=MODALITY.edition.ano)

    return render(request, 'area-admin/../../templates/pages/adminPanel/competidores/modalidades.html', locals())


@staff_member_required
def dashboard_admin_category(request, modality_id):
    modality_edition = ModalityEdition.objects.get(id=modality_id)
    category_modality = CategoryModality.objects.filter(modality_edition=modality_edition)
    page_number = request.GET.get('page')
    items_per_page = 3  # Altere o número de categorias por página conforme desejado

    paginator = Paginator(category_modality, items_per_page)
    page_obj = paginator.get_page(page_number)

    for category in page_obj:

        if request.GET.get('completed'):
            inscriptions = CompetitorsRegistration.objects.filter(
                registration__lot__category_modality=category,
                registration__status='3').order_by(
                'registration')
            registration_ids = inscriptions.values_list('registration__id', flat=True)

        elif request.GET.get('uncompleted'):
            inscriptions = CompetitorsRegistration.objects.filter(
                registration__lot__category_modality=category
            ).exclude(
                Q(registration__status='3') | Q(registration__status='4')
            ).order_by('registration')
            registration_ids = inscriptions.values_list('registration__id', flat=True)
        else:
            inscriptions = CompetitorsRegistration.objects.filter(
                registration__lot__category_modality=category).order_by(
                'registration')
            registration_ids = inscriptions.values_list('registration__id', flat=True)
        if request.GET.get('search'):
            # Busca as inscrições pelo número de inscrição
            search_query = request.GET.get('search')
            inscriptions = inscriptions.annotate(
                full_name=Concat('user__first_name', Value(' '), 'user__last_name')
            ).filter(
                Q(full_name__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(registration__registration_number__icontains=search_query)
            )
            registration_ids = inscriptions.values_list('registration__id', flat=True)
        category.inscritos = inscriptions.count()  # Conta o número de inscritos em cada competição
        registrations = Registration.objects.filter(id__in=registration_ids)

        # new_inscription = CompetitorsRegistration.objects.filter(registration__in=registrations)
        category.registration = registrations
        category.inscricoes = inscriptions
        for register in category.registration:
            same_inscriptions = inscriptions.filter(registration=register)
            names = ' - '.join(same_inscriptions.values_list('user__first_name', flat=True))
            register.names = names
            register.order = Order.objects.get(registration=register)
            try:
                payment_history = PaymentHistory.objects.filter(order=register.order).latest('created_at')
            except PaymentHistory.DoesNotExist:
                payment_history = PaymentHistory.objects.create(order=register.order, transaction_status='PENDING')

            # payment_history, created = PaymentHistory.objects.get_or_create(order=register.order, defaults={
            #     'transaction_status': 'PENDING',
            # })
            register.history = payment_history
        category.documents = []
        modality_edition = ModalityEdition.objects.get(id=category.modality_edition.id)
        documentos_modality_edition = modality_edition.documents.all()
        for document in documentos_modality_edition:
            category.documents.append(document)

    form = AdminPaymentForm()
    recuse_form = AdminRecuseDocumentForm()
    registration_form = RegistrationAdminForm()
    lot_form = LotAdminForm()
    return render(request, 'area-admin/../../templates/pages/adminPanel/competidores/competidores.html', locals())


@staff_member_required
def dashboard_admin_check_scanner(request):
    return render(request, 'area-admin/../../templates/pages/adminPanel/check_scanner.html', locals())


@staff_member_required
def dashboard_admin_checkin(request, competitor_registration, edition_id):
    competitor_registration = competitor_registration or None
    edition_id = edition_id or None
    competitor_registration = CompetitorsRegistration.objects.get(pk=competitor_registration)
    edition = Edition.objects.get(pk=edition_id)

    check_list = CheckList.objects.get(id=edition.check_list.id)
    competitor_check_list, _ = CompetitorCheckList.objects.get_or_create(
        competitor_registration=competitor_registration,
        check_list=check_list)

    checklist_items = competitor_check_list.check_list_item_concluded.all()
    all_checklist_items = check_list.checklistitem_set.all()

    return render(request, 'area-admin/../../templates/pages/adminPanel/checkin.html', locals())


@staff_member_required
def checkin_list(request):
    ultima_edicao = Edition.objects.filter(status='3').order_by('-ano').first()
    modality = ModalityEdition.objects.filter(edition=ultima_edicao)
    selected_modality_id = request.GET.get('modality_id')

    if selected_modality_id:
        selected_modality = ModalityEdition.objects.get(id=selected_modality_id)
        category_modality = CategoryModality.objects.filter(modality_edition=selected_modality)
    else:
        selected_modality = None
        category_modality = CategoryModality.objects.filter(modality_edition__edition=ultima_edicao)

    competitors = CompetitorsRegistration.objects.filter(
        registration__lot__category_modality__in=category_modality
    ).order_by('user__username')  # Substitua 'user__username' pela coluna que deseja usar para a ordenação
    list_item = CheckListItem.objects.filter(checklist=ultima_edicao.check_list.id)

    # Configuração da paginação
    page = request.GET.get('page', 1)
    paginator = Paginator(competitors, 20)  # Divida os competidores em grupos de 10 por página

    try:
        competitors_page = paginator.page(page)
    except PageNotAnInteger:
        competitors_page = paginator.page(1)
    except EmptyPage:
        competitors_page = paginator.page(paginator.num_pages)

    # Passa a modalidade selecionada para o template para preservar a seleção
    selected_modality_id = int(selected_modality_id) if selected_modality_id else None
    return render(request, 'area-admin/../../templates/pages/adminPanel/competidores/checkin_list.html', {
        'ultima_edicao': ultima_edicao,
        'modality': modality,
        'category_modality': category_modality,
        'competitors': competitors_page,  # Use a página atual de competidores
        # 'competitor_check_list': competitor_check_list,
        'list_item': list_item,
        'selected_modality': selected_modality,
        'selected_modality_id': selected_modality_id,
    })


def format_price_with_commas(price):
    price = float(f"{price:.2f}")
    price_str = str(price)
    parts = price_str.split('.')
    whole_part = parts[0]
    decimal_part = ',' + parts[1] if len(parts) > 1 else ''
    # Adiciona a pontuação a cada grupo de 3 dígitos na parte inteira do preço
    formatted_price = ''
    for i in range(len(whole_part), 0, -3):
        group = whole_part[max(i - 3, 0):i]
        if formatted_price != '':
            formatted_price = group + '.' + formatted_price
        else:
            formatted_price = group

    # Remove o ponto de separação no início se necessário
    formatted_price = formatted_price.lstrip('.')

    # Concatena a parte inteira com a parte decimal, se houver
    formatted_price += decimal_part

    return formatted_price


from django.db.models import Sum, Case, When, Value, IntegerField


@staff_member_required
def dashboard_admin(request):
    # Obter o valor das vendas por mês
    vendas_por_mes = PaymentHistory.objects.filter(transaction_status='CONFIRMED').annotate(
        mes=ExtractMonth('created_at')
    ).values('mes').annotate(
        valor_total=Sum('amount')
    ).order_by('mes')

    # Criar um dicionário com os valores das vendas por mês
    vendas_dict = {venda['mes']: str(venda['valor_total']) if venda['valor_total'] is not None else 0.00 for venda in
                   vendas_por_mes}
    vendas = json.dumps(vendas_dict)

    return render(request, 'area-admin/../../templates/pages/adminPanel/home.html', locals())


@api_view(['GET'])
def get_dados_periodo(request):
    periodo_inicio = request.GET.get('periodo_inicio')
    periodo_fim = request.GET.get('periodo_fim')

    pagamentos = PaymentHistory.objects.all()

    if periodo_inicio and periodo_fim:
        # Converter as strings de data para objetos datetime
        periodo_inicio = datetime.strptime(periodo_inicio, '%Y-%m-%d').date()
        periodo_fim = datetime.strptime(periodo_fim, '%Y-%m-%d').date()

        # Filtrar os objetos PaymentHistory por período
        pagamentos = pagamentos.filter(transaction_date__date__gte=periodo_inicio,
                                       transaction_date__date__lte=periodo_fim)

    # Calcular os valores agregados
    total_arrecadado = pagamentos.filter(transaction_status='CONFIRMED').aggregate(Sum('amount'))['amount__sum'] or 0.0
    valor_pendente = pagamentos.exclude(transaction_status='CONFIRMED').aggregate(Sum('amount'))['amount__sum'] or 0.0
    numero_pedidos = pagamentos.count()

    # Filtrar as inscrições por período
    inscricoes = Registration.objects.all()
    if periodo_inicio and periodo_fim:
        inscricoes = inscricoes.filter(created_at__date__gte=periodo_inicio, created_at__date__lte=periodo_fim)
    numero_inscricoes = inscricoes.count()

    # Filtrar os competidores por período
    competidores = CompetitorsRegistration.objects.all()
    if periodo_inicio and periodo_fim:
        competidores = competidores.filter(created_at__date__gte=periodo_inicio, created_at__date__lte=periodo_fim)
    numero_competidores = competidores.count()

    # Filtrar as equipes por período
    equipes = Team.objects.all()
    if periodo_inicio and periodo_fim:
        equipes = equipes.filter(created_at__date__gte=periodo_inicio, created_at__date__lte=periodo_fim)
    numero_equipes = equipes.count()

    dados = {
        'total_arrecadado': "R$ " + formatar_valor(total_arrecadado),
        'numero_pedidos': numero_pedidos,
        'valor_pendente': "R$ " + formatar_valor(valor_pendente),
        'numero_inscricoes': numero_inscricoes,
        'numero_competidores': numero_competidores,
        'numero_equipes': numero_equipes,
    }
    return JsonResponse(dados)


@staff_member_required
def update_registration_category(request, registration_id=None, modality_id=None):
    obj = get_object_or_404(Registration, id=registration_id)
    admin_form = LotAdminForm(request.POST, instance=obj)

    if request.method == 'POST' and admin_form.is_valid():
        if admin_form.is_valid():
            obj.lot = admin_form.cleaned_data['lot']
            admin_form.save()
        else:
            print(admin_form.errors)

    return redirect(reverse('dashboard_admin_category', kwargs={'modality_id': modality_id}))


@staff_member_required
def update_history_payment(request, payment_id=None, modality_id=None):
    obj = get_object_or_404(PaymentHistory, id=payment_id)
    admin_form = AdminPaymentForm(request.POST, instance=obj)
    if request.method == 'POST' and admin_form.is_valid():
        if admin_form.is_valid():
            obj.billing_type = admin_form.cleaned_data['billing_type']
            admin_form.save()
        else:
            print(admin_form.errors)

    if admin_form.is_valid():
        return JsonResponse({
            "success": True,
            "amount": obj.amount,
            "split": obj.split_condictions,
            "status": obj.get_transaction_status_display(),
            "payment": obj.get_billing_type_display()
        })
    else:
        errors = {}
        if isinstance(admin_form.errors, ErrorDict):
            errors.update(dict(admin_form.errors))
        return JsonResponse({"success": False, "errors": errors})


@staff_member_required
def update_registration_remake(request, payment_id=None, modality_id=None):
    obj = get_object_or_404(PaymentHistory, id=payment_id)
    registration_form = RegistrationAdminForm(request.POST, instance=obj.order.registration)
    regis = None

    if request.method == 'POST' and registration_form.is_valid():
        regis = Registration.objects.get(id=obj.order.registration.id)
        regis.status = registration_form.cleaned_data['status']
        registration_form.save()

    if registration_form.is_valid():
        return JsonResponse({
            "success": True,
            "id": regis.id,
            "status": regis.get_status_display()
        })
    else:
        errors = {}
        if isinstance(registration_form.errors, ErrorDict):
            errors.update(dict(registration_form.errors))
        return JsonResponse({"success": False, "errors": errors})


def aprove_document(request):
    if request.method == 'POST':
        document_id = request.POST.get('document_id')
        competitor_id = request.POST.get('competitor_id')
        competitor_registration_id = request.POST.get('competitor_registration_id')
        registration_document = get_object_or_404(
            RegistrationDocuments,
            document_type_id=document_id,
            competitor_registration_id=competitor_registration_id,
            user_id=competitor_id
        )
        registration_document.approval_status = '3'
        registration_document.save()
        return JsonResponse({'message': 'Documento aprovado com sucesso!',
                             'document_name': registration_document.document_type.title})

    return JsonResponse({'message': 'Método inválido'})


def recuse_document(request, doc_slug, user_id, registration_id):
    recuse_form = AdminRecuseDocumentForm(request.POST or None)
    if request.method == 'POST' and recuse_form.is_valid():
        email_list = []
        user = get_object_or_404(User, id=user_id)
        email_list.append(user.email)
        template = 'pages/adminPanel/competidores/recuse_document.html'
        html = render_to_string(template, {'competitor_name': user.get_full_name(),
                                           'recuse_reason': recuse_form.cleaned_data['recuse_reason']})
        plain_message = strip_tags(html)
        threading.Thread(
            target=send_email_async,
            kwargs={
                "subject": 'Documento Recusado',
                "message": plain_message,
                "html_message": html,
                "recipient_list": email_list
            }).start()
        doc = get_object_or_404(Document, slug=doc_slug)
        registration_document = get_object_or_404(
            RegistrationDocuments,
            document_type_id=doc.id,
            competitor_registration_id=registration_id,
            user_id=user_id
        )
        registration_document.approval_status = '4'
        registration_document.save()
        return JsonResponse({'success': True,
                             'document_name': registration_document.document_type.title, })
    return JsonResponse({'message': 'Método inválido'})


def exportar_xlsx(request):
    query = """
    SELECT
  CONCAT(uu.first_name, ' ', uu.last_name) AS Nome,
  uu.email,
  uu.phone AS Telefone,
  uu.birthdate AS DataNascimento,
  FLOOR(DATEDIFF(CURDATE(), uu.birthdate) / 365) AS Idade,
  uu.country AS Pais,
  uu.city AS Cidade,
  uu.uf AS Estado,
  uu.neighborhood AS Bairro,
  uu.address as Endereco,
  uu.cep AS CEP,
 CASE
  WHEN uu.cep BETWEEN '01000-000' AND '39999-999' THEN 'Região Sudeste'
  WHEN uu.cep BETWEEN '40000-000' AND '65999-999' THEN 'Região Nordeste'
  WHEN uu.cep BETWEEN '66000-000' AND '68899-999' THEN 'Região Norte'
  WHEN uu.cep BETWEEN '68900-000' AND '68999-999' THEN 'Região Norte'
  WHEN uu.cep BETWEEN '69000-000' AND '69299-999' THEN 'Região Norte'
  WHEN uu.cep BETWEEN '69300-000' AND '69399-999' THEN 'Região Norte'
  WHEN uu.cep BETWEEN '69400-000' AND '69899-999' THEN 'Região Norte'
  WHEN uu.cep BETWEEN '69900-000' AND '69999-999' THEN 'Região Norte'
  WHEN uu.cep BETWEEN '76800-000' AND '76999-999' THEN 'Região Norte'
  WHEN uu.cep BETWEEN '77000-000' AND '77999-999' THEN 'Região Norte'
  WHEN uu.cep BETWEEN '70000-000' AND '72799-999' THEN 'Região Centro-Oeste'
  WHEN uu.cep BETWEEN '72800-000' AND '72999-999' THEN 'Região Centro-Oeste'
  WHEN uu.cep BETWEEN '73000-000' AND '73699-999' THEN 'Região Centro-Oeste'
  WHEN uu.cep BETWEEN '73700-000' AND '76799-999' THEN 'Região Centro-Oeste'
  WHEN uu.cep BETWEEN '78000-000' AND '78899-999' THEN 'Região Centro-Oeste'
  WHEN uu.cep BETWEEN '79000-000' AND '79999-999' THEN 'Região Centro-Oeste'
  WHEN uu.cep BETWEEN '80000-000' AND '87999-999' THEN 'Região Sul'
  WHEN uu.cep BETWEEN '88000-000' AND '89999-999' THEN 'Região Sul'
  WHEN uu.cep BETWEEN '90000-000' AND '99999-999' THEN 'Região Sul'
  ELSE 'Região Desconhecida'
END AS Regiao,
  fl.price AS Preco,
  ccoe.name AS Modalidade,
  ccc.name AS Categoria,
  cr.sponsorship AS Patrocinador,
  cr.registration_number,
  crv.name AS Veiculo,
  b.name AS Marca,
  tb.name AS MarcaPneu,
  cr.wheel_rim AS Aro,
  ct.name AS Equipe,
  DATE(cc.created_at) AS DataInscricao,  
  TIME(cc.created_at) AS HorarioInscricao,  
  CASE cr.status
    WHEN 1 THEN 'Registro'
    WHEN 2 THEN 'Pago'
    WHEN 3 THEN 'Homologado'
    ELSE 'Cancelado'
  END AS Status
FROM
  `competitor_competitorsregistration` cc
  LEFT JOIN `users_user` uu ON cc.user_id = uu.id
  LEFT JOIN `competitor_registration` cr ON cc.registration_id = cr.id
  LEFT JOIN `financial_lot` fl ON cr.lot_id = fl.id
  LEFT JOIN `competition_categorymodality` ccm ON fl.category_modality_id = ccm.id
  LEFT JOIN `competition_competitioncategory` ccc ON ccm.category_id = ccc.id
  LEFT JOIN `competition_modalityedition` cme ON ccm.modality_edition_id = cme.id
  LEFT JOIN `competition_competitionmodality` ccoe ON cme.modality_id = ccoe.id
  LEFT JOIN `competitor_vehiclemodel` crv ON cr.vehicle_model_id = crv.id
  LEFT JOIN `competitor_vehiclebrand` b ON crv.brand_id = b.id
  LEFT JOIN `competitor_tirebrand` tb ON cr.tire_brand_id = tb.id
    LEFT JOIN `competitor_team` ct ON cr.team_id=ct.id
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="export.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    headers = ['Nome', 'Email', 'Telefone', 'Aniversario', 'Idade', 'Pais', 'Cidade', 'Estado', 'Bairro', 'Endereco',
               'CEP',
               'Regiao', 'Preco', 'Modalidade', 'Categoria', 'Patrocinador', 'Numero de Registro', 'Veiculo', 'Marca',
               'Marca Pneu', 'Aro', 'Equipe', 'Data da Inscricao', 'Horario Inscricao', 'Status']

    worksheet.append(headers)

    for row in rows:
        worksheet.append(row)

    output = io.BytesIO()
    save_workbook(workbook, output)
    response_excel = HttpResponse(output.getvalue(),
                                  content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response_excel['Content-Disposition'] = 'attachment; filename="export.xlsx"'
    return response_excel


def exportar_xlsx_modalidty(request, modality_edition_id):
    query = """
    SELECT
        CONCAT(uu.first_name, ' ', uu.last_name) AS Nome,
        uu.email,
        uu.phone AS Telefone,
        uu.birthdate AS DataNascimento,
        FLOOR(DATEDIFF(CURDATE(), uu.birthdate) / 365) AS Idade,
        uu.country AS Pais,
        uu.city AS Cidade,
        uu.uf AS Estado,
        uu.neighborhood AS Bairro,
        uu.address as Endereco,
        uu.cep AS CEP,
        CASE
            WHEN uu.cep BETWEEN '01000-000' AND '39999-999' THEN 'Região Sudeste'
            WHEN uu.cep BETWEEN '40000-000' AND '65999-999' THEN 'Região Nordeste'
            WHEN uu.cep BETWEEN '66000-000' AND '68899-999' THEN 'Região Norte'
            WHEN uu.cep BETWEEN '68900-000' AND '68999-999' THEN 'Região Norte'
            WHEN uu.cep BETWEEN '69000-000' AND '69299-999' THEN 'Região Norte'
            WHEN uu.cep BETWEEN '69300-000' AND '69399-999' THEN 'Região Norte'
            WHEN uu.cep BETWEEN '69400-000' AND '69899-999' THEN 'Região Norte'
            WHEN uu.cep BETWEEN '69900-000' AND '69999-999' THEN 'Região Norte'
            WHEN uu.cep BETWEEN '76800-000' AND '76999-999' THEN 'Região Norte'
            WHEN uu.cep BETWEEN '77000-000' AND '77999-999' THEN 'Região Norte'
            WHEN uu.cep BETWEEN '70000-000' AND '72799-999' THEN 'Região Centro-Oeste'
            WHEN uu.cep BETWEEN '72800-000' AND '72999-999' THEN 'Região Centro-Oeste'
            WHEN uu.cep BETWEEN '73000-000' AND '73699-999' THEN 'Região Centro-Oeste'
            WHEN uu.cep BETWEEN '73700-000' AND '76799-999' THEN 'Região Centro-Oeste'
            WHEN uu.cep BETWEEN '78000-000' AND '78899-999' THEN 'Região Centro-Oeste'
            WHEN uu.cep BETWEEN '79000-000' AND '79999-999' THEN 'Região Centro-Oeste'
            WHEN uu.cep BETWEEN '80000-000' AND '87999-999' THEN 'Região Sul'
            WHEN uu.cep BETWEEN '88000-000' AND '89999-999' THEN 'Região Sul'
            WHEN uu.cep BETWEEN '90000-000' AND '99999-999' THEN 'Região Sul'
            ELSE 'Região Desconhecida'
        END AS Regiao,
        fl.price AS Preco,
        ccoe.name AS Modalidade,
        ccc.name AS Categoria,
        cr.sponsorship AS Patrocinador,
        cr.registration_number,
        crv.name AS Veiculo,
        b.name AS Marca,
        tb.name AS MarcaPneu,
        cr.wheel_rim AS Aro,
        ct.name AS Equipe,
        DATE(cc.created_at) AS DataInscricao,  
        TIME(cc.created_at) AS HorarioInscricao,  
        CASE cr.status
            WHEN 1 THEN 'Registro'
            WHEN 2 THEN 'Pago'
            WHEN 3 THEN 'Homologado'
            ELSE 'Cancelado'
        END AS Status
    FROM
        competitor_competitorsregistration cc
        LEFT JOIN users_user uu ON cc.user_id = uu.id
        LEFT JOIN competitor_registration cr ON cc.registration_id = cr.id
        LEFT JOIN financial_lot fl ON cr.lot_id = fl.id
        LEFT JOIN competition_categorymodality ccm ON fl.category_modality_id = ccm.id
        LEFT JOIN competition_competitioncategory ccc ON ccm.category_id = ccc.id
        LEFT JOIN competition_modalityedition cme ON ccm.modality_edition_id = cme.id
        LEFT JOIN competition_competitionmodality ccoe ON cme.modality_id = ccoe.id
        LEFT JOIN competitor_vehiclemodel crv ON cr.vehicle_model_id = crv.id
        LEFT JOIN competitor_vehiclebrand b ON crv.brand_id = b.id
        LEFT JOIN competitor_tirebrand tb ON cr.tire_brand_id = tb.id
        LEFT JOIN competitor_team ct ON cr.team_id = ct.id
    WHERE cme.id = {}
    """.format(modality_edition_id)

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    connection.close()

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="export-modalitys.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    headers = ['Nome', 'Email', 'Telefone', 'Aniversario', 'Idade', 'Pais', 'Cidade', 'Estado', 'Bairro', 'Endereco',
               'CEP',
               'Regiao', 'Preco', 'Modalidade', 'Categoria', 'Patrocinador', 'Numero de Registro', 'Veiculo', 'Marca',
               'Marca Pneu', 'Aro', 'Equipe', 'Data da Inscricao', 'HorarioInscricao', 'Status']

    worksheet.append(headers)

    for row in rows:
        worksheet.append(row)

    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    response.write(output.read())
    return response


def get_champions_data(request, selected_year):
    # Perform a query to get the champions data for the selected year
    champions_data = CompetitorsRegistration.objects.filter(
        registration__lot__category_modality__modality_edition__edition__ano=selected_year).values(
        'category', 'name', 'sponsorship', 'state', 'vehicle'
    )

    # Convert the queryset to a list of dictionaries
    champions_list = list(champions_data)

    return JsonResponse(champions_list, safe=False)


def galeria_dos_compeoes(request):
    form = ChampionEditionForm(request.POST or None)
    selected_edition = form.cleaned_data['edition'] if request.method == 'POST' and form.is_valid() else None
    if selected_edition == '':
        champions = Champion.objects.all().order_by('-edition')
    elif selected_edition:
        selected_year = int(selected_edition.split(' - ')[-1])
        champions = Champion.objects.filter(edition=selected_year)
    else:
        latest_edition = Champion.objects.aggregate(Max('edition'))['edition__max']
        champions = Champion.objects.filter(edition=latest_edition)

    champions_data = {}
    for champion in champions:
        modality = champion.modality
        if modality not in champions_data:
            champions_data[modality] = []
        champions_data[modality].append(champion)

    return render(request, 'pages/galeria-dos-campeoes.html', {
        'form': form,
        'selected_edition': selected_edition,
        'champions_data': champions_data,
    })


def process_document(document, latest_active_edition_subquery, errors):
    filename_parts = document.name.split('.')
    if len(filename_parts) > 0:
        try:
            number = int(filename_parts[0])
            competitor_registration = CompetitorsRegistration.objects.filter(
                number=number,
                registration__lot__category_modality__modality_edition__edition__id__in=Subquery(
                    latest_active_edition_subquery)
            ).first()
            if competitor_registration:
                Boleto.objects.create(competitor_registration=competitor_registration, document_file=document)
            else:
                errors.append(
                    f"Nenhuma CompetitorsRegistration correspondente encontrada para o número {number} e edição ativa.")
        except Exception as e:
            errors.append(f"Erro ao processar o documento '{document.name}': {str(e)}")


@staff_member_required
def upload_documents(request):
    if request.method == 'POST' and request.FILES.getlist('documents'):
        documents = request.FILES.getlist('documents')
        latest_active_edition_subquery = Edition.objects.filter(
            event_start_date__lte=datetime.now(),
            event_end_date__gte=datetime.now(),
            status=3
        ).order_by('-event_start_date').values('pk')[:1]

        errors = []

        batch_size = 20
        batches = [documents[i:i + batch_size] for i in range(0, len(documents), batch_size)]

        for batch in batches:
            for document in batch:
                process_document(document, latest_active_edition_subquery, errors)
        return render(request, 'pages/upload_documents.html', {'errors': errors})

    else:
        return render(request, 'pages/upload_documents.html', )


def newsletter_send_email(request):
    form = NewsletterForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        interest_area = form.cleaned_data['interest_area'].name  # Acesso ao nome da CompetitionModality selecionada
        Newsletter.objects.create(email=email, interest_area=interest_area)
        return redirect('home')
    else:
        return redirect('home')


@api_view(['GET'])
def delete_registration_blank(request):
    orphaned_orders_count = 0
    orphaned_registrations_count = 0

    orders = Order.objects.all()
    for order in orders:
        if not order.registration.competitorsregistration_set.exists():
            order.delete()
            orphaned_orders_count += 1

    registrations = Registration.objects.all()
    for registration in registrations:
        if not registration.competitorsregistration_set.exists():
            registration.delete()
            orphaned_registrations_count += 1

    return Response({
        'orphaned_orders_deleted': orphaned_orders_count,
        'orphaned_registrations_deleted': orphaned_registrations_count
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def atualizar_banners(request):
    today = date.today()
    banners = Banner.objects.all()

    count_active = 0
    count_deactivated = 0
    for banner in banners:
        if banner.start_date <= today <= banner.end_date:
            banner.is_active = True
            count_active += 1
        else:
            banner.is_active = False
            count_deactivated += 1
        banner.save()

    return Response({'banner_change_active': count_active,
                     'banner_change_deactivated': count_deactivated,
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def pizza_chart(request):
    period = request.GET.get('period')  # Obter o período selecionado (7, 30, 90)
    if period == 'all':
        # Não aplicar filtro de data
        count_pagamentos_pendentes = PaymentHistory.objects.filter(
            transaction_status='PENDING'
        ).count()

        count_pagamentos_confirmados = PaymentHistory.objects.filter(
            transaction_status='CONFIRMED',
            order__status=2
        ).count()
    else:
        # Calcular a data de início com base no período selecionado
        end_date = datetime.now()

        if period == '7':
            start_date = end_date - timedelta(days=7)
        elif period == '30':
            start_date = end_date - timedelta(days=30)
        elif period == '90':
            start_date = end_date - timedelta(days=90)
        else:
            return JsonResponse({'error': 'Período inválido'})
        # Contar os pagamentos pendentes
        count_pagamentos_pendentes = PaymentHistory.objects.filter(
            transaction_status='PENDING',
            transaction_date__gte=start_date,
            transaction_date__lte=end_date
        ).count()

        # Contar os pagamentos confirmados
        count_pagamentos_confirmados = PaymentHistory.objects.filter(
            transaction_status='CONFIRMED',
            order__status=2,
            transaction_date__gte=start_date,
            transaction_date__lte=end_date
        ).count()

    # Retornar os dados em formato JSON
    data = {
        'labels': ['Pendentes', 'Confirmados'],
        'data': [count_pagamentos_pendentes, count_pagamentos_confirmados],
    }
    return JsonResponse(data)


def formatar_valor(valor):
    if valor is None:
        return "Sem valor"

    partes = str(valor).split('.')
    inteiro = partes[0]
    decimal = partes[1] if len(partes) > 1 else '00'

    inteiro_formatado = ''
    contador = 0
    for digito in inteiro[::-1]:
        if contador != 0 and contador % 3 == 0:
            inteiro_formatado = '.' + inteiro_formatado
        inteiro_formatado = digito + inteiro_formatado
        contador += 1

    decimal_formatado = decimal[:2]  # Limita para no máximo 2 casas decimais

    return f'{inteiro_formatado},{decimal_formatado}'


@api_view(['GET'])
def get_payment_data(request):
    # Obtenha os dados dos pagamentos do banco de dados
    payments = PaymentHistory.objects.values('billing_type').annotate(
        pending_amount=Sum('amount', filter=Q(transaction_status='PENDING')),
        paid_amount=Sum('amount', filter=Q(transaction_status='CONFIRMED')),
        total_amount=Sum('amount'),
        pending_competitors=Count('id', filter=Q(transaction_status='PENDING')),
        total_competitors=Count('id'),
    )

    # Crie um dicionário com as opções de pagamento
    payment_form_dict = dict(PAYMENT_FORM)

    # Crie uma lista com os dados de cada método de pagamento
    payment_data = []
    for payment in payments:
        billing_type = payment['billing_type']
        billing_type_display = payment_form_dict.get(billing_type,
                                                     "Pagamento não informado")  # Obtém o valor formatado do campo billing_type
        paid_amount = formatar_valor(payment['paid_amount'])
        pending_amount = formatar_valor(payment['pending_amount'])
        total_amount = formatar_valor(payment['total_amount'])
        payment_data.append({
            'payment_method': billing_type_display,
            'paid_amount': paid_amount,
            'pending_amount': pending_amount,
            'total_amount': total_amount,
            'pending_competitors': payment['pending_competitors'],
            'total_competitors': payment['total_competitors'],
        })

    # Retorne os dados em formato JSON
    return JsonResponse(payment_data, safe=False)


def download_ficha(request, registration_id):
    registration = Registration.objects.get(id=registration_id)
    return render(request, 'pages/competitorPanel/ficha_competidor.html', locals())
