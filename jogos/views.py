from django.shortcuts import render

from .models import Athlete, Modality, Stage, Results
from .serializer import AthleteSerializer, ModalitySerializer, StageSerializer, ResultsSerializer

from rest_framework import status
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

    def create(self, request, *args, **kwargs):
        """
        Only will be permitted add results if stage is True (in progress). 
        If stage = False (finished) add results will be forbidden.
        """
        stage = request.data['stage']
        stage_status = Stage.objects.get(id=stage).status

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if stage in modality is finished
        if stage_status:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        else:
            context = {
                "mensagem": "Esta etapa da competição já encontra-se encerrada."
            }
            return Response(context, status=status.HTTP_403_FORBIDDEN)

        # Preciso verificar tambem se uma etapa esta relacionada a uma modalidade