from django.shortcuts import render

from .models import Athlete, Modality, Stage, Results
from .serializer import AthleteSerializer, ModalitySerializer, StageSerializer, ResultsSerializer

from rest_framework import status
from rest_framework import viewsets, permissions, generics, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Max, Subquery, Min, Count, Sum

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

    @action(detail=True, methods=['get'])
    def ranking(self, request, pk=None):
        """
        Show the ranking of athletes in stage of competition
        """
        pk = self.kwargs['pk']
        stage = self.get_object()

        modality = Stage.objects.get(id=self.kwargs['pk']).modality

        if 'Dardo' in modality.name or 'dardo' in modality.name:
            queryset = Results.objects.filter(stage=pk, active=True).order_by('-value')
            serializer = ResultsSerializer(queryset, many=True)
        else:
            serializer = ResultsSerializer(Results.objects.filter(stage=pk).order_by('value'), many=True)
        
        #print(serializer.data)
        return Response(enumerate(serializer.data, start=1))
        


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
            self.best_value_athlete(chances_athlete, serializer, len_results)
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
        

    @staticmethod
    def best_value_athlete(chances_athlete, serializer, len_results):
        """
        Method that will compare the values of result for each athlete and define the best value
        Modality: Lançamento de Dardos only
        """
        if len_results > 0:
            result_bd = chances_athlete.filter(active=True).first()
            pk_result_bd = result_bd.pk
            result_value_bd = result_bd.value

            recent_result = Results.objects.last()
            pk_recent_result = recent_result.pk

            if result_value_bd > float(serializer.data['value']):
                recent_result.active=False
                recent_result.save()
            else:
                result_bd.active=False
                result_bd.save()