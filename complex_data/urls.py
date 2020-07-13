from django.urls import path, include
from rest_framework.routers import DefaultRouter
from complex_data import views


router = DefaultRouter()
router.register('data', views.DataViewSet, basename='data')


urlpatterns = [
    path('', include(router.urls)),
]
