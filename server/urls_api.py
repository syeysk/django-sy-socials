from django.urls import path, include


urlpatterns = [
    path('', include('django_sy_framework.base.urls_api')),
]
