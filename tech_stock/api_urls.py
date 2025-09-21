from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('assets/', include('assets.urls')),
    path('inventory/', include('inventory.urls')),
    path('reports/', include('reports.urls')),
    path('sales/', include('sales.urls')),
]