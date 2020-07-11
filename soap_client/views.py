from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from requests import Session
from requests.auth import HTTPBasicAuth
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import zeep
from nav_info import settings
from soap_client.serializers import (
    DeviceSerializer, DriverSerializer, DeviceGroupSerializer)
from zeep.cache import InMemoryCache
from zeep.transports import Transport


class RawViewSet(viewsets.ViewSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        session = Session()
        session.auth = HTTPBasicAuth(settings.NAV_USER, settings.NAV_PASS)

        self.client = zeep.Client(settings.NAV_HOST,
                                  transport=Transport(session=session,
                                                      cache=InMemoryCache()))

    @action(detail=False)
    @swagger_auto_schema(responses={
        200: DeviceSerializer(many=True,
                              help_text="Структура, содержащая данные по автомобилю")})
    def getAllDevices(self, request):
        """
        Метод возвращает список автомобилей компании, к которой принадлежит пользователь, осуществляющий запрос
        """
        soap_res = self.client.service.getAllDevices()
        serializer = DeviceSerializer(soap_res, many=True)
        return Response(serializer.data)

    @action(detail=False)
    @swagger_auto_schema(responses={
        200: DriverSerializer(many=True,
                              help_text="Структура, содержащая данные по водителю")})
    def getAllDrivers(self, request):
        """
        Метод возвращает список водителей, определенных для компании. Идентификаторы сквозные
        """
        soap_res = self.client.service.getAllDrivers()
        serializer = DriverSerializer(soap_res, many=True)
        return Response(serializer.data)

    @action(detail=False)
    @swagger_auto_schema(responses={
        200: DeviceGroupSerializer(many=True,
                                   help_text="Структура содержит данные по группе (клиенту)")})
    def getAllDeviceGroups(self, request):
        """
        Метод возвращает все группы компании, к которой принадлежит пользователь, осуществляющий запрос
        """
        soap_res = self.client.service.getAllDeviceGroups()
        serializer = DeviceGroupSerializer(soap_res, many=True)
        return Response(serializer.data)
