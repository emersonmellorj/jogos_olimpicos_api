from django.shortcuts import render

from .models import Athlete, Modality, Stage, Results
from .serializer import AthleteSerializer, ModalitySerializer, StageSerializer, ResultsSerializer

from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response

class AthleteViewSet(viewsets.ModelViewSet):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer

    
class ModalityViewSet(viewsets.ModelViewSet):
    queryset = Modality.objects.all()
    serializer_class = ModalitySerializer

    @action(detail=True, methods=['get'])
    def athletes(self, request, pk=None):
        """
        Function with action that will allow the creation of route modality/athletes
        """
        modality = self.get_object()
        serializer = AthleteSerializer(modality.athletes.all(), many=True)
        print(serializer.data)
        return Response(serializer.data)


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer


class ResultsViewSet(viewsets.ModelViewSet):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer