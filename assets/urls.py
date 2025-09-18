from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComputerModelViewSet, ComputerViewSet

router = DefaultRouter()
router.register(r'computer-models', ComputerModelViewSet, basename='computermodel')
router.register(r'computers', ComputerViewSet, basename='computer')

urlpatterns = [path('', include(router.urls))]