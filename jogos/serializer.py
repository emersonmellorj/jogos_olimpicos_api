from rest_framework import serializers
from .models import Athlete, Modality, Stage, Results

class AthleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Athlete
        fields = (
            'id',
            'first_name',
            'last_name',
            'age',
            'created_in',
            'active'
        )