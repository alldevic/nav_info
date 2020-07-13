from django.urls import path, include
from rest_framework.routers import DefaultRouter
from soap_client import views


router = DefaultRouter()
router.register('raw', views.RawViewSet, basename='raw')
router.register('data', views.DataViewSet, basename='data')


urlpatterns = [
    path('', include(router.urls)),
]
