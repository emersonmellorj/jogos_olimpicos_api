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

        # Checking if stage is registered for the chosen modality
        obj_stage = Stage.objects.filter(modality=request.data["modality"])
        relationship = False
        for data in obj_stage:
            if int(request.data["stage"]) == data.id:
                relationship = True

        """
        Each athlete have 3 chances in "Lançamento de Dardo" for each stage
        Each athlete have 1 chance in "100m Rasos" for each stage
        """
        chances_athlete = Results.objects.filter(
            stage=stage, 
            modality=request.data["modality"], 
            athlete=request.data["athlete"]
        ) 
        len_results = len([chance.value for chance in chances_athlete])
        modality_name = Modality.objects.get(pk=request.data["modality"]).name
        have_chances = False

        if len_results == 0:
            have_chances = True
        elif len_results < 3:
            if '100m' in modality_name:
                have_chances = False
            elif len_results <= 2:
                have_chances = True

        # Validations before add result in DB
        if stage_status and relationship and have_chances:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        else:
            if relationship == False:
                context = {
                    "mensagem": "Esta etapa não pertence a modalidade escolhida."
                }
            elif stage_status == False:
                context = {
                    "mensagem": "Esta etapa da competição já encontra-se encerrada."
                }
            else:
                context = {
                    "mensagem": "Para esta etapa e modalidade ja existe(m) resultado(s) cadastrado(s) para o atleta."
                }
            
            return Response(context, status=status.HTTP_403_FORBIDDEN)
