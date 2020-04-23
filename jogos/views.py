from django.shortcuts import render

from .models import Athlete, Modality, Stage, Results
from .serializer import AthleteSerializer

from rest_framework import viewsets, permissions, generics

class AthleteViewSet(viewsets.ModelViewSet):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer