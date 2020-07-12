from django.urls import path, include
from rest_framework.routers import DefaultRouter
from soap_client import views


router = DefaultRouter()
router.register('raw', views.RawViewSet, basename='raw')


urlpatterns = [
    path('', include(router.urls)),
]
