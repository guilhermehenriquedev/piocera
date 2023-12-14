import pprint
import xml.etree.ElementTree as ET
from collections import namedtuple

import requests
from competition.models import ModalityEdition, CategoryModality, Edition, \
    Banner
from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from financial.asaas_customer import update_client, create_client
from financial.asaas_payment import create_charge, get_charge, gera_pix_key
from financial.forms import CreditCardForm, OrderForm, CreditCardHolderInfo
from financial.models import Lot, Order, PaymentHistory, AccountBank
from users.models import User

from .forms import RegistrationForm, CompetitorRegistrationForm, \
    RegistrationDocumentsForm, UserProfileForm, ZequinhaApoioForm
from .models import Team, Registration, CompetitorsRegistration, \
    Document, RegistrationDocuments, VehicleModel, \
    TeamMembers, CheckListItem, CompetitorCheckList, Boleto
from django.db.models import Q
from django.utils import timezone
from itertools import groupby
from operator import attrgetter


@login_required
def inicio_area_competidor(request):
    competitor = request.user

    try:
        last_registration = CompetitorsRegistration.objects.filter(
            user=competitor
        ).latest('id')

    except ObjectDoesNotExist:
        pass

    edition = Edition.objects.latest('created_at')
    banners = Banner.objects.filter(edition=edition).count()

    try:

        competitor_registrations = CompetitorsRegistration.objects.filter(
            user=competitor,
        ).order_by('-created_at')

        for competitor_registration in competitor_registrations:
            registration = competitor_registration.registration
            lot = Lot.objects.get(registration=registration)
            category_modality = CategoryModality.objects.get(id=lot.category_modality.id)
            modality_edition = ModalityEdition.objects.get(id=category_modality.modality_edition.id)
            competitor_registration.documents = []
            competitor_registration.documents_approved = []
            documentos_modality_edition = modality_edition.documents.all()
            for documento in documentos_modality_edition:
                competitor_registration.documents.append(documento)
                registration_document = RegistrationDocuments.objects.filter(document_type=documento, user=competitor)
                for doc in registration_document:
                    if doc.approval_status == '3':
                        competitor_registration.documents_approved.append(documento)
    except ObjectDoesNotExist:
        competitor_registrations = None
        documents = None

    try:
        registration_documents = RegistrationDocuments.objects.filter(
            user=competitor,
            approval_status='3'
        )
    except ObjectDoesNotExist:
        registration_documents = 0
    return render(request, 'pages/competitorPanel/my_subscriptions.html', locals())


@login_required
def area_competidor(request, registration_id, competitor_registration_id):
    competitor = get_object_or_404(User, pk=request.user.pk)
    registration = get_object_or_404(Registration, id=registration_id)
    competitor_registration = get_object_or_404(CompetitorsRegistration, id=competitor_registration_id, user=competitor)
    lot = Lot.objects.get(registration=registration)
    category_modality = CategoryModality.objects.get(
        id=lot.category_modality.id
    )
    modality_edition = ModalityEdition.objects.get(
        id=category_modality.modality_edition.id
    )
    documents = modality_edition.documents

    list_type_competitor_completed = []
    falta_candidato = False
    if modality_edition.type_competitors.count() > CompetitorsRegistration.objects.filter(
            registration=registration).count():
        falta_candidato = True
    try:
        registration_documents = RegistrationDocuments.objects.filter(
            user=competitor
        )
    except ObjectDoesNotExist:
        registration_documents = 0
    count_registration_documents = registration_documents.filter(approval_status='3').count()
    try:
        payment_history = PaymentHistory.objects.filter(
            order__registration=registration_id
        ).latest('created_at')  # correção do erro de pagamento

    except ObjectDoesNotExist:
        payment_history = None

    list_item = CheckListItem.objects.filter(checklist=modality_edition.edition.check_list.id)
    competitor_check_list = CompetitorCheckList.objects.filter(
        competitor_registration=competitor_registration)

    return render(request, 'pages/competitorPanel/competitor_area.html', locals())


@login_required
def competitor_boletos(request):
    user = request.user
    boletos_list = Boleto.objects.filter(competitor_registration__user=user).order_by('-created_at')
    boletos = {}
    for boleto in boletos_list:
        boletos.setdefault(boleto.created_at.date(), []).append(boleto)
    return render(request, 'pages/competitorPanel/competitor_boletos.html', locals())


@login_required
def editar_conta(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'As informações do competidor foram atualizadas '
                             'com sucesso!')
        else:
            messages.error(request, form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'pages/competitorPanel/my_personal_data.html', locals())


@login_required
def lista_competidores(request):
    try:
        # Buscar a edição mais recente ativa
        latest_active_edition = Edition.objects.filter(status=3).latest('created_at')


        # Buscar os registros de competidores da edição ativa
        competitor_registration_list = CompetitorsRegistration.objects.filter(
            registration__lot__category_modality__modality_edition__edition=latest_active_edition
        ).order_by('registration__lot__category_modality')

        # Agrupar os registros de competidores por category_modality
        groupby_key = attrgetter('registration.lot.category_modality')
        competitor_registration_list = [
            (key, list(group)) for key, group in groupby(competitor_registration_list, groupby_key)
        ]
    except ObjectDoesNotExist:
        competitor_registration_list = None
    return render(request, 'pages/competitorPanel/competitors_list.html', locals())

from django.core.exceptions import ValidationError
@login_required
def registrar_documento_inscricao(request, competitor_registration_id, document_type_id):
    competitor_registration = get_object_or_404(CompetitorsRegistration, id=competitor_registration_id)
    document_type = get_object_or_404(Document, id=document_type_id)

    if request.method == 'POST':
        file = request.FILES.get('document_file')
        if file and file.content_type not in ['image/png', 'image/jpeg', 'application/pdf']:
            messages.error(request, 'Formato de documento não aceito!')
            return redirect('area-competidor', registration_id=competitor_registration.registration.id, competitor_registration_id=competitor_registration.id)


        registration_document = RegistrationDocuments.objects.filter(user=request.user,
                                                                     competitor_registration=competitor_registration,
                                                                     document_type=document_type).first()
        if registration_document:
            form = RegistrationDocumentsForm(request.POST, request.FILES, instance=registration_document)
        else:
            form = RegistrationDocumentsForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.competitor_registration = competitor_registration
            f.document_type = document_type
            f.approval_status = '2'
            f.save()
            messages.success(request, 'As informações do competidor foram atualizadas com sucesso!')

    if 'next' in request.GET:
        return redirect(request.GET['next'])
    return JsonResponse({'status': 'ok'}, safe=False)


def modality(request, ano):
    modalities = ModalityEdition.objects.filter(edition__ano=ano).order_by('position')
    return render(request, 'pages/modality.html', locals())


from datetime import date, datetime


def calcular_idade(user, tipo, edition_date):
    edition_date = datetime(edition_date.year, edition_date.month, edition_date.day)

    # CBC e CBM conta no ANO
    if 'testes' in tipo:
        try:
            birth = datetime(user.birthdate.year, user.birthdate.month, user.birthdate.day)
            if birth:
                age = edition_date.year - birth.year - (
                        (edition_date.month, edition_date.day) < (birth.month, birth.day))
                return age
            else:
                age = None
        except AttributeError:
            age = None
        return age
    else:
        try:
            birth = datetime(user.birthdate.year, user.birthdate.month, user.birthdate.day)
            today = date.today()
            if birth:
                age = (today.year + 1) - birth.year
            else:
                age = None
        except AttributeError:
            age = None
        return age


def format_price_with_commas(price):
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


def category(request, ano, slug_modalidade):
    current_time = timezone.now()

    categories = CategoryModality.objects.prefetch_related('lot_set').filter(
        modality_edition__modality__slug=slug_modalidade,
        modality_edition__edition__ano=ano,
        lot__start_date__lte=current_time,  # Lote começa antes ou no mesmo momento que a data atual
        lot__end_date__gte=current_time  # Lote termina depois ou no mesmo momento que a data atual
    ).annotate(valid_lot=Q(lot__start_date__lte=current_time) & Q(lot__end_date__gte=current_time))

    categories = categories.filter(valid_lot=True)
    modality = ModalityEdition.objects.get(modality__slug=slug_modalidade, edition__ano=ano)
    user = request.user
    edition = get_object_or_404(Edition, ano=ano)
    age = calcular_idade(user, slug_modalidade, edition.edition_date)

    for category in categories:
        for lot in category.lot_set.all():
            lot.price = format_price_with_commas(lot.price)  # Atualizar o preço do lote em 10% de desconto

    return render(request, 'pages/category.html', locals())


@login_required()
def inscricao_competicao(request, ano, slug_modalidade, slug_categoria, lot_slug):
    category_modality = get_object_or_404(CategoryModality,
                                          category__slug=slug_categoria,
                                          modality_edition__modality__slug=slug_modalidade,
                                          modality_edition__edition__ano=ano)
    type_m_all = category_modality.modality_edition.type_competitors.all()
    type_m = [t.name for t in type_m_all]
    try:
        lot = Lot.lots.get(slug=lot_slug)
    except Lot.DoesNotExist:
        messages.error(request, 'O lote escolhido expirou, por favor selecione uma opção abaixo válida.')
        return redirect(reverse('category', kwargs={'ano': ano, 'slug_modalidade': slug_modalidade}))

    if request.method == 'POST':
        data = request.POST.copy()
        data['lot'] = lot
        user = request.user
        form = RegistrationForm(data)
        context = {'form': form, 'ano': ano, 'category_modality': category_modality}
        if form.is_valid():
            create_team_name = form.cleaned_data.get('create_team_name', None)
            team_member = form.cleaned_data.get('team_member', None)

            team = form.cleaned_data.get('team', None)
            if create_team_name:
                team = Team.objects.create(name=create_team_name, coordinator=user)
                form.instance.team = team

            if team:
                TeamMembers.objects.create(team=team, user=user, member_position=team_member)

            registration = form.save(commit=False)
            lot = registration.lot
            user = request.user
            lot_full = False
            if lot.category_modality.number_vacancies <= lot.registration_set.count():
                form.add_error('lot', 'Este lote não possui mais vagas disponíveis.')
                lot_full = True
            if user and lot and CompetitorsRegistration.objects.filter(user=user, registration__lot=lot).exists():
                if lot_full:
                    form.errors['lot'].append('Voce ja esta registrado nesse lote.')
                else:
                    form.add_error('lot', 'Voce ja esta registrado nesse lote.')

            if form.errors:
                return render(request, 'pages/competition_data.html', context)
            else:
                form.save(commit=True)
                Order.objects.create(registration=registration, lot=lot)

            return redirect(reverse('register_pilot', kwargs={
                'ano': ano,
                'slug_modalidade': slug_modalidade,
                'slug_categoria': slug_categoria,
                'lot_slug': lot.slug,
                'inscricao': registration.id,
            }))

        else:
            print(form.errors)
    else:
        form = RegistrationForm()

    context = {'form': form, 'ano': ano, 'category_modality': category_modality, 'lot': lot, 'type_m': type_m}
    return render(request, 'pages/competition_data.html', context)


@login_required()
def buscar_cpf(request):
    try:
        user = User.objects.get(cpf=request.GET.get('cpf'))
        user_dict = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'nickname': user.nickname,
            'rg': user.rg,
            # 'cpf': user.cpf,
            'clothing': user.clothing,
            'birthdate': user.birthdate,
            'cep': user.cep,
            'country': user.country,
            'uf': user.uf,
            'city': user.city,
            'neighborhood': user.neighborhood,
            'address': user.address,
            'phone': user.phone,
            'allergy': user.allergy,
            'organ_expedidor': user.organ_expedidor,
            'federation': user.federation.id if user.federation else None,
            'name_emergency_contact': user.name_emergency_contact,
            'emergency_phone': user.emergency_phone,
            'blood_type': user.blood_type,
            'national_license': user.national_license,
            'health_insurance_plan': user.health_insurance_plan,
            'cnh': user.cnh,
            'lgpd_acceptance': user.lgpd_acceptance,
            'profile_foto': user.profile_foto.url if user.profile_foto else None,
        }
        return JsonResponse(user_dict)
    except User.DoesNotExist:
        return JsonResponse({'detail': False})


def get_vehicle_models(request, brand_id):
    vehicle_models = VehicleModel.objects.filter(brand_id=brand_id).values('id', 'name')
    return JsonResponse({model['id']: model['name'] for model in vehicle_models})


@login_required()
def register_pilot(request, ano, slug_modalidade, slug_categoria, lot_slug, inscricao):
    category_modality = get_object_or_404(CategoryModality,
                                          category__slug=slug_categoria,
                                          modality_edition__modality__slug=slug_modalidade,
                                          modality_edition__edition__ano=ano)
    edition = Edition.objects.latest('ano')
    try:
        lot = Lot.lots.get(slug=lot_slug)
    except Lot.DoesNotExist:
        messages.error(request, 'O lote escolhido expirou, por favor selecione uma opção abaixo válida.')
        return redirect('category', ano=ano, slug_modalidade=slug_modalidade)
    user = request.user

    register_completed = CompetitorsRegistration.objects.filter(registration__id=inscricao)
    list_register_complete = [register_complete.type for register_complete in register_completed]
    missing_types = [type_m for type_m in category_modality.modality_edition.type_competitors.all() if
                     type_m not in list_register_complete]

    missing_types_id = [type_m.id for type_m in missing_types]

    registration = get_object_or_404(Registration, id=inscricao)

    if not category_modality.modality_edition.modality.is_apoio_zequinha:
        form = CompetitorRegistrationForm(missing_types_id, request.POST or None)
    else:
        form = ZequinhaApoioForm(missing_types_id, request.POST or None)

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data.copy()
        full_name = data.pop('full_name', '')
        name_parts = full_name.strip().split(' ', maxsplit=1)

        try:
            user = User.objects.get(cpf=data['cpf'])
            ## ativar IF caso precise restringir atualização dos dados por pessoa logada
            # if request.user.cpf == user.cpf:
            for field, value in data.items():
                setattr(user, field, value)

            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            user.save()
        except User.DoesNotExist:
            messages.error(request,
                           'Por conta da Lei de Proteção de Dados, para prosseguir com a inscrição deste competidor, '
                           'é necessário que seja criado uma conta utilizando o seu CPF. Após isso, você poderá dar continuidade a inscrição')
            return redirect('register_pilot', ano=ano, slug_modalidade=slug_modalidade,
                            slug_categoria=slug_categoria, lot_slug=lot.slug, inscricao=registration.id)
        if user and lot and CompetitorsRegistration.objects.filter(user=user,
                                                                   registration__lot__category_modality__modality_edition__edition=edition).exists():
            form.add_error('cpf', 'Esse usuário está inscrito em uma Modalidade, para solicitar uma alteração '
                                  'voce deve solicitar para a equipe Radical.')
            if form.errors:
                return render(request, 'pages/competitor_data.html', locals())
        birthdate = user.birthdate
        if category_modality.has_age and birthdate is not None:

            event_start_date = category_modality.modality_edition.edition.event_start_date.date()
            today = date.today()
            age = (event_start_date.year - birthdate.year)
            if age < category_modality.min_age or age > category_modality.max_age:
                messages.error(request,
                               f'Você não se enquadra na faixa etária desta categoria. A idade desse competidor'
                               f' no ano do evento seria {age} anos. Faixa etária do evento: {category_modality.min_age} '
                               f'- {category_modality.max_age} anos.')
                return redirect('register_pilot', ano=ano, slug_modalidade=slug_modalidade,
                                slug_categoria=slug_categoria, lot_slug=lot.slug, inscricao=registration.id)

        if CompetitorsRegistration.objects.filter(user=user, registration=registration).exists():
            messages.error(request, 'Você já está registrado nesta competição.')
            return redirect('register_pilot', ano=ano, slug_modalidade=slug_modalidade,
                            slug_categoria=slug_categoria, lot_slug=lot.slug, inscricao=registration.id)
        competitor = form.save(commit=False)
        competitor.user = user
        competitor.registration = registration
        competitor.type = data['type']
        competitor.save()
        order_exist = Order.objects.filter(registration=registration, lot=lot).exists()

        if not category_modality.modality_edition.modality.is_apoio_zequinha:
            missing_types.remove(data['type'])

        if missing_types and not category_modality.modality_edition.modality.is_apoio_zequinha:
            return redirect('register_pilot', ano=ano, slug_modalidade=slug_modalidade,
                            slug_categoria=slug_categoria, lot_slug=lot.slug, inscricao=registration.id)
        elif order_exist:
            return redirect('payment_type', ano=ano, slug_modalidade=slug_modalidade,
                            slug_categoria=slug_categoria, lot_slug=lot.slug, inscricao=registration.id)
        else:
            return redirect('competitor_area.html')
    else:
        print(form.errors)
    can_skip_registration = register_completed.exists() and missing_types
    context = {
        'form': form,
        'ano': ano,
        'slug_modalidade': slug_modalidade,
        'slug_categoria': slug_categoria,
        'lot_slug': lot_slug,
        'inscricao': registration.id,
        'category_modality': category_modality,
        'lot': lot,
        'type_m': [type_m.name for type_m in category_modality.modality_edition.type_competitors.all()],
        'can_skip_registration': can_skip_registration,
        'edition': edition
    }
    return render(request, 'pages/competitor_data.html', context)


def token_pagseguro(itemId1, itemDescription1, itemAmount1, itemQuantity1, reference, senderEmail, senderName):
    endpoint = config("PAGSEGURO_API") + "checkout"
    params = {
        "email": config("PAGSEGURO_EMAIL"),
        "token": config("PAGSEGURO_TOKEN")
    }
    xml_content = """
   <checkout>
      <sender>
        <name>""" + senderName + """</name>
        <email>""" + senderEmail + """</email>
      </sender>
      <currency>BRL</currency>
      <items>
        <item>
          <id>""" + reference + """</id>
          <description>""" + itemDescription1 + """</description>
          <amount>""" + itemAmount1 + """</amount>
          <quantity>""" + itemQuantity1 + """</quantity>
        </item>
      </items>
      <redirectURL>https://piocera.com.br/inscricao/competitor_area.html/</redirectURL>
      <reference>""" + reference + """</reference>
      <timeout>100</timeout>
      <maxAge>999999999</maxAge>
      <maxUses>1</maxUses>
      <receiver>
        <email>""" + config("PAGSEGURO_EMAIL") + """</email>
      </receiver>
      <enableRecover>false</enableRecover>
    </checkout>
    """

    headers = {"Content-Type": "application/xml"}

    response = requests.post(endpoint, params=params, data=xml_content, headers=headers)
    if response.status_code == 200:
        root = ET.fromstring(response.text)

        code_element = root.find('code')
        code = code_element.text
        return code
    else:
        print(f"Erro na geração do token: {response.status_code} - {response.text}")
        return None


def payment_pagseguro(request, inscricao, lot_slug):
    ## pega o pedido e inscrição, caso nao tenha pode so gerar um pedido novo
    registration = get_object_or_404(Registration, id=inscricao)

    lot = Lot.lots.get(slug=lot_slug)

    order, created_order = Order.objects.get_or_create(registration=registration, lot=lot)

    ## pega o usuario que se inscreveu e que está logado
    registration_competitor = CompetitorsRegistration.objects.filter(registration=registration)
    user_registration_competitor = registration_competitor.filter(user=request.user)

    itemId1 = str(registration.id)
    itemDescription1 = str(
        registration.registration_number) + ' - ' + lot.category_modality.category.name + ' - ' + lot.category_modality.modality_edition.modality.name
    itemAmount1 = str(lot.price)
    itemQuantity1 = "1"
    reference = str(registration.registration_number)
    senderEmail = registration_competitor[0].user.email
    senderName = registration_competitor[0].user.first_name + ' ' + registration_competitor[0].user.last_name

    external_url = config("REDIRECT_CHECKOUT") + "?code=" + token_pagseguro(itemId1, itemDescription1, itemAmount1,
                                                                            itemQuantity1, reference, senderEmail,
                                                                            senderName)
    return HttpResponseRedirect(external_url)
    # category_modality = get_object_or_404(CategoryModality,
    #                                       category__slug=slug_categoria,
    #                                       modality_edition__modality__slug=slug_modalidade,
    #                                       modality_edition__edition__ano=ano)
    # ## verifica os tipos de competidores daquela modalidade-categoria
    # type_m_all = category_modality.modality_edition.type_competitors.all()
    # type_m = [t.name for t in type_m_all]
    # type_m_id = [t.id for t in type_m_all]
    #
    # ## valida o lote
    # try:
    #     lot = Lot.lots.get(slug=lot_slug)
    #     parcelas = Lot.installments.payment_installment(lot)
    # except Lot.DoesNotExist:
    #     messages.error(request, 'O lote escolhido expirou, por favor selecione uma opção abaixo válida.')
    #     return redirect(reverse('category', kwargs={'ano': ano, 'slug_modalidade': slug_modalidade}))
    #
    # ## dados bancarios ativos da radical
    # account_bank = AccountBank.objects.filter(is_active=True)
    # if account_bank.exists():
    #     account_bank = account_bank[0]
    #
    # ## pega o pedido e inscrição, caso nao tenha pode so gerar um pedido novo
    # registration = get_object_or_404(Registration, id=inscricao)
    # order, created_order = Order.objects.get_or_create(registration=registration, lot=lot)
    #
    # ## pega o usuario que se inscreveu e que está logado
    # registration_competitor = CompetitorsRegistration.objects.filter(registration=registration)
    # user_registration_competitor = registration_competitor.filter(user=request.user)


from decimal import Decimal, ROUND_DOWN


def payment_type(request, ano, slug_modalidade, slug_categoria, lot_slug, inscricao):
    category_modality = get_object_or_404(CategoryModality,
                                          category__slug=slug_categoria,
                                          modality_edition__modality__slug=slug_modalidade,
                                          modality_edition__edition__ano=ano)

    ## verifica os tipos de competidores daquela modalidade-categoria
    type_m_all = category_modality.modality_edition.type_competitors.all()
    type_m = [t.name for t in type_m_all]
    type_m_id = [t.id for t in type_m_all]

    ## valida o lote
    try:
        lot = Lot.lots.get(slug=lot_slug)
        parcelas = Lot.installments.payment_installment(lot)
    except Lot.DoesNotExist:
        messages.error(request, 'O lote escolhido expirou, por favor selecione uma opção abaixo válida.')
        return redirect(reverse('category', kwargs={'ano': ano, 'slug_modalidade': slug_modalidade}))

    ## dados bancarios ativos da radical
    account_bank = AccountBank.objects.filter(is_active=True)
    if account_bank.exists():
        account_bank = account_bank[0]

    ## pega o pedido e inscrição, caso nao tenha pode so gerar um pedido novo
    registration = get_object_or_404(Registration, id=inscricao)
    order, created_order = Order.objects.get_or_create(registration=registration, lot=lot)

    ## pega o usuario que se inscreveu e que está logado
    registration_competitor = CompetitorsRegistration.objects.filter(registration=registration)
    user_registration_competitor = registration_competitor.filter(user=request.user)

    ## cria o historico ou recupera um histórico de pagamento
    payment_history, created = PaymentHistory.objects.get_or_create(order=order,
                                                                    amount=lot.price)

    valor_90_percent = Decimal(lot.price) * Decimal("0.9")
    full_name_user = request.user.get_full_name()

    lot.price = format_price_with_commas(lot.price)
    valor_90_percent = valor_90_percent.quantize(Decimal("0.00"), rounding=ROUND_DOWN)
    value_discont_final = format_price_with_commas(valor_90_percent)
    return render(request, 'pages/payment.html', locals())

# return render(request, 'competitor/formaDePagamento.html', {'form': form, 'ano': ano, 'category_modality': category_modality, 'lot': lot, 'type_m_': type_m_id})
