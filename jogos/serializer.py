from rest_framework import serializers
from .models import Athlete, Modality, Stage, Results


class Base(serializers.ModelSerializer):
    """
    Base Class for serializers classes
    """
    modality_name = serializers.ReadOnlyField(source="modality.name")
    stage_name = serializers.ReadOnlyField(source="stage.name")
    stage_status = serializers.ReadOnlyField(source="stage.status")
    first_name_athlete = serializers.ReadOnlyField(source="athlete.first_name")
    last_name_athlete = serializers.ReadOnlyField(source="athlete.last_name")

    class Meta:
        abstract=True


class AthleteSerializer(Base):
    class Meta:
        extra_kwargs = {
            'modality': {'write_only': True}
        }
        model = Athlete
        fields = (
            'id',
            'first_name',
            'last_name',
            'modality',
            'modality_name',
            'age',
            'created_in',
            'active'
        )


class StageSerializer(Base):
    """
    In portuguese: Etapa
    """
    #modality_name = serializers.ReadOnlyField(source="modality.name")
    class Meta:
        extra_kwargs = {
            'modality': {'write_only': True}
        }
        model = Stage
        fields = (
            'id',
            'name',
            'modality',
            'modality_name',
            'status',
            'created_in',
            'updated_in',
            'active',
        )


class ModalitySerializer(serializers.ModelSerializer):
    """
    This serializer will show the modalities, stages and the athletes registered in each modality
    """
    athletes = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='athlete-detail')
    stages_modality = StageSerializer(many=True, read_only=True)

    class Meta:
        model = Modality
        fields = (
            'id',
            'name',
            'athletes',
            'stages_modality',
            'created_in',
            'active',
        )


class ResultsSerializer(Base):
    """
    Fields for show the names of Objects in return of Results
    """
    class Meta:
        extra_kwargs = {
            'modality': {'write_only': True},  
            'stage': {'write_only': True}, 
            'athlete': {'write_only': True}
        }
        model = Results
        fields = (
            "id",
            "modality",
            "modality_name",
            "stage",
            "stage_name",
            "stage_status",
            "athlete",
            "first_name_athlete",
            "last_name_athlete",
            "value",
            "unity",
            "created_in"
        )