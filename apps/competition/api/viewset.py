from rest_framework import status, viewsets, generics, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import filters
from competition.api.serializer import EditionSerializer, FederationSerializer, SponsorSerializer, BannerSerializer, \
    WebSiteEditionSerializer, CompetitionModalitySerializer, ModalityEditionSerializer, CompetitionCategorySerializer, \
    CategoryModalitySerializer
from competition.models import Edition, Federation, Sponsor, Banner, WebSiteEdition, CompetitionModality, \
    ModalityEdition, CompetitionCategory, CategoryModality
from django.db.models import Prefetch

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny


class EditionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer
    permission_classes = [IsAdminUser]


class FederationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Federation.objects.all()
    serializer_class = FederationSerializer
    permission_classes = [IsAdminUser]


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsAdminUser]


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminUser]


class WebSiteEditionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WebSiteEdition.objects.all()
    serializer_class = WebSiteEditionSerializer
    permission_classes = [IsAdminUser]


class CompetitionModalityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompetitionModality.objects.all()
    serializer_class = CompetitionModalitySerializer
    permission_classes = [IsAdminUser]


class ModalityEditionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModalityEdition.objects.all()
    serializer_class = ModalityEditionSerializer
    permission_classes = [IsAdminUser]


class CompetitionCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompetitionCategory.objects.all()
    serializer_class = CompetitionCategorySerializer
    permission_classes = [IsAdminUser]


class CategoryModalityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoryModality.objects.all()
    serializer_class = CategoryModalitySerializer
    permission_classes = [IsAdminUser]
