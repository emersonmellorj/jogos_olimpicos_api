from rest_framework import serializers
from .models import Athlete, Modality, Stage, Results

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = (
            'id',
            'first_name',
            'last_name',
            'modality',
            'age',
            'created_in',
            'active'
        )


class ModalitySerializer(serializers.ModelSerializer):
    """
    This serializer will show the modalities and the athletes registered in each modality
    """
    #athletes = AthleteSerializer(many=True, read_only=True)
    athletes = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='athlete-detail')

    class Meta:
        model = Modality
        fields = (
            'id',
            'name',
            'athletes',
            'created_in',
            'active',
        )


class StageSerializer(serializers.ModelSerializer):
    """
    In portuguese: Etapa
    """
    class Meta:
        model = Stage
        fields = (
            'id',
            'name',
            'modality',
            'status',
            'created_in',
            'active',
        )


class MyRelatedField(serializers.RelatedField):
    def to_representation(self, obj):
        return {
            'id': obj.pk,
        }

class ResultsSerializer(serializers.ModelSerializer):
    modality_name = serializers.ReadOnlyField(source="modality.name")
    stage_name = serializers.ReadOnlyField(source="stage.name")
    first_name = serializers.ReadOnlyField(source="athlete.first_name")
    last_name = serializers.ReadOnlyField(source="athlete.last_name")
    class Meta:
        model = Results
        fields = (
            "id",
            "modality_name",
            "stage_name",
            "first_name",
            "last_name",
            "value",
            "unity",
            "created_in"
        )