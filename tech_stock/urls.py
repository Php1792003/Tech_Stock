from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('techstock/', include('tech_stock.api_urls')),
]