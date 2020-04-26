from django.shortcuts import render

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework import status, viewsets, permissions, generics, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Athlete, Modality, Stage, Results
from .serializer import AthleteSerializer, ModalitySerializer, StageSerializer, ResultsSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

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
        self.pagination_class.page_size = 10
        athlete = Athlete.objects.filter(athlete_id=pk)
        page = self.paginate_queryset(athlete)

        if page is not None:
            serializer = AthleteSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        modality = self.get_object()
        serializer = AthleteSerializer(modality.athletes.all(), many=True)
        print(serializer.data)
        return Response(serializer.data)


class StageViewSet(viewsets.ModelViewSet):
    """
    The ViewSet StageViewSet has cache in Redis for requisitions to this endpoint
    """
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @action(detail=True, methods=['get'])
    def ranking(self, request, pk=None):
        """
        Show the ranking of athletes in stage of competition
        """
        self.pagination_class.page_size = 10

        pk = self.kwargs['pk']
        stage = self.get_object()

        modality = Stage.objects.get(id=self.kwargs['pk']).modality

        if 'Dardo' in modality.name or 'dardo' in modality.name:
            results = Results.objects.filter(stage=pk, active=True).order_by('-value')
            page = self.paginate_queryset(results)

            if page is not None:
                serializer = ResultsSerializer(page, many=True)
                return self.get_paginated_response(enumerate(serializer.data, start=1))

            queryset = Results.objects.filter(stage=pk, active=True).order_by('-value')
            serializer = ResultsSerializer(queryset, many=True)

        else:
            results = Results.objects.filter(stage=pk).order_by('value')
            page = self.paginate_queryset(results)

            if page is not None:
                serializer = ResultsSerializer(page, many=True)
                return self.get_paginated_response(enumerate(serializer.data, start=1))

            serializer = ResultsSerializer(Results.objects.filter(stage=pk).order_by('value'), many=True)
        
        return Response(enumerate(serializer.data, start=1))
        

class ResultsViewSet(viewsets.ModelViewSet):
    """
    The ViewSet ResultsViewSet has cache in Redis for requisitions to this endpoint
    """
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Only will be permitted add results if stage is True (in progress). 
        If stage = False (finished) add results will be forbidden.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Checking if stage is registered for the chosen modality
        obj_stage = Stage.objects.filter(modality=request.data["modality"])
        relationship = False
        for data in obj_stage:
            if int(request.data["stage"]) == data.id:
                relationship = True

        # Checking if athlete is registered for the chosen modality
        obj_athlete = Athlete.objects.get(pk=request.data['athlete'])
        modality_for_athlete = False
        if obj_athlete.modality_id == int(request.data["modality"]):
            modality_for_athlete = True
        
        """
        Each athlete has 3 chances in "Lançamento de Dardo" for each stage
        Each athlete has 1 chance in "100m Rasos" for each stage
        """
        stage = request.data['stage']
        stage_status = Stage.objects.get(id=stage).status
        chances_athlete = Results.objects.filter(
            stage=stage, modality=request.data["modality"], athlete=request.data["athlete"]
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
        return_data = self.validate_create_data(stage_status, relationship, have_chances, 
                                                modality_for_athlete, serializer, chances_athlete, len_results)

        if 'mensagem' not in return_data:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=return_data)
        else:
            return Response(return_data, status=status.HTTP_403_FORBIDDEN)

    def validate_create_data(self, stage_status, relationship, have_chances, 
                            modality_for_athlete, serializer, chances_athlete, len_results):
        """
        Method that validate data before save in DB
        """
        if stage_status and relationship and have_chances and modality_for_athlete:
            self.perform_create(serializer)
            self.best_value_athlete(chances_athlete, serializer, len_results)
            headers = self.get_success_headers(serializer.data)
            return headers
        
        else:
            if relationship == False:
                context = {
                    "mensagem": "Esta etapa não pertence a modalidade escolhida."
                }
            elif stage_status == False:
                context = {
                    "mensagem": "Esta etapa da competição já encontra-se encerrada."
                }
            elif modality_for_athlete == False:
                context = {
                    "mensagem": "Este atleta não pertence à modalidade escolhida."
                }
            else:
                context = {
                    "mensagem": "Para esta etapa e modalidade ja existe(m) resultado(s) cadastrado(s) para o atleta."
                }
            return context

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