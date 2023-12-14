from rest_framework import status, viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.http import require_POST
from rest_framework import filters

from rest_framework.views import APIView

from django.db.models import Prefetch
from competitor.models import CompetitorCheckList, CheckList, CheckListItem, CompetitorsRegistration, CompetitorCheckListItem
from competitor.api.serializer import CompetitorCheckListSerializer, CompetitorCheckListGetSerializer

from competition.models import Edition

from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required


class CompetitorCheckListViewSets(viewsets.ModelViewSet):
    queryset = CompetitorCheckList.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['competitor_registration', ]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return CompetitorCheckListGetSerializer
        return CompetitorCheckListSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = CompetitorCheckListGetSerializer(instance).data
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = CompetitorCheckListGetSerializer(instance).data
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# @csrf_exempt
@staff_member_required
def removeCheckListItemFromCompetitor(request, competitor_checklist_id, checklist_item_id):
    if request.method == 'POST':
        competitor_checklist = get_object_or_404(CompetitorCheckList, id=competitor_checklist_id)
        checklist_item = get_object_or_404(CheckListItem, id=checklist_item_id)

        competitor_checklist.check_list_item_concluded.remove(checklist_item)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Método inválido'})
@staff_member_required
@require_POST
def createCompetitorCheckListItem(request, competitor_checklist_id, checklist_item_id):
    competitor_checklist = get_object_or_404(CompetitorCheckList, id=competitor_checklist_id)
    checklist_item = get_object_or_404(CheckListItem, id=checklist_item_id)

    # Verifique se o item de checklist já foi concluído pelo competidor
    if checklist_item not in competitor_checklist.check_list_item_concluded.all():
        # Se não foi concluído, crie um CompetitorCheckListItem
        image = request.FILES.get('image')
        if image:
            CompetitorCheckListItem.objects.create(
                competitor_checklist=competitor_checklist,
                check_list_item=checklist_item,
                confirmation_image=image  # Supondo que a imagem seja enviada como um arquivo
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Nenhuma imagem fornecida'})
    else:
        return JsonResponse({'error': 'Item de checklist já concluído pelo competidor'})


# @csrf_exempt
@staff_member_required
def addCheckListItemToCompetitorCheckList(request, competitor_checklist_id, checklist_item_id):
    if request.method == 'POST':
        competitor_checklist = get_object_or_404(CompetitorCheckList, id=competitor_checklist_id)
        checklist_item = get_object_or_404(CheckListItem, id=checklist_item_id)

        competitor_checklist.check_list_item_concluded.add(checklist_item)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Método inválido'})


class CompetitorCheckListRetrieveOrCreateViewSets(generics.RetrieveAPIView):
    serializer_class = CompetitorCheckListSerializer
    queryset = CompetitorCheckList.objects.all()

    def get_object(self):
        competitor_registration = self.kwargs.get('competitor_registration', None)
        edition_id = self.kwargs.get('edition_id', None)
        competitor_registration = CompetitorsRegistration.objects.get(pk=competitor_registration)
        edition = Edition.objects.get(pk=edition_id)

        check_list = CheckList.objects.get(id=edition.check_list.id)
        obj, _ = self.get_queryset().get_or_create(
            competitor_registration=competitor_registration,
            check_list=check_list)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
