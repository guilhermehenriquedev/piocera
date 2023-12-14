from rest_framework import serializers

from competitor.models import TypeCompetitor, CompetitorCheckList, CheckList, CheckListItem, CompetitorsRegistration


class TypeCompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCompetitor
        fields = "__all__"


class CompetitorsRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitorsRegistration
        fields = "__all__"


class CheckListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckListItem
        fields = "__all__"


class CheckListSerializer(serializers.ModelSerializer):
    items = CheckListItemSerializer(many=True, read_only=True, source='checklistitem_set')

    class Meta:
        model = CheckList
        fields = "__all__"


class CompetitorCheckListGetSerializer(serializers.ModelSerializer):
    competitor_registration = CompetitorsRegistrationSerializer(many=False, read_only=True)
    check_list = CheckListSerializer(many=False, read_only=True)
    check_list_item_concluded = CheckListItemSerializer(many=True, read_only=True)

    class Meta:
        model = CompetitorCheckList
        fields = "__all__"


class CompetitorCheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitorCheckList
        fields = "__all__"
