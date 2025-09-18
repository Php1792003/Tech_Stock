from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PositionViewSet, DepartmentViewSet, EmployeeViewSet

router = DefaultRouter()
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]