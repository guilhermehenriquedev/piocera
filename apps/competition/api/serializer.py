from rest_framework import serializers

from competition.models import Edition, Federation, Sponsor, Banner, WebSiteEdition, CompetitionModality, \
    ModalityEdition, CompetitionCategory, CategoryModality
from competitor.api.serializer import TypeCompetitorSerializer


class EditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edition
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'type' in data and data['type']:
            data['type'] = instance.get_type_display()
        if 'status' in data and data['status']:
            data['status'] = instance.get_status_display()
        return data


class FederationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Federation
        fields = "__all__"


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'type' in data and data['type']:
            data['type'] = instance.get_type_display()
        return data


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'position' in data and data['position']:
            data['position'] = instance.get_position_display()
        return data


class WebSiteEditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebSiteEdition
        fields = "__all__"


class CompetitionModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionModality
        fields = "__all__"


class CompetitionModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionModality
        fields = "__all__"


class ModalityEditionSerializer(serializers.ModelSerializer):
    type_competitors = TypeCompetitorSerializer(many=True, read_only=True)

    class Meta:
        model = ModalityEdition
        fields = "__all__"


class CompetitionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionCategory
        fields = "__all__"


class CategoryModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModality
        fields = "__all__"
