from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import (
    AthleteViewSet
)

"""
Routers
"""
router = SimpleRouter()
router.register('athletes', AthleteViewSet)

url_patterns = router.urls