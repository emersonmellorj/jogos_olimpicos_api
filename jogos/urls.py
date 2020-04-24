from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import (
    AthleteViewSet,
    ModalityViewSet,
    StageViewSet,
    ResultsViewSet
)

"""
Routers
"""
router = SimpleRouter()
router.register('athletes', AthleteViewSet)
router.register('modality', ModalityViewSet)
router.register('stage', StageViewSet)
router.register('results', ResultsViewSet)

url_patterns = router.urls