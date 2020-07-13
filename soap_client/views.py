from drf_yasg.utils import swagger_auto_schema
from requests import Session
from requests.auth import HTTPBasicAuth
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import zeep
from nav_info import settings
from soap_client.negotiation import IgnoreClientContentNegotiation
from soap_client.serializers import (ChannelDescriptorSerializer,
                                     DeviceGroupSerializer, DeviceSerializer,
                                     DriverSerializer, GeoZoneSerializer,
                                     GetAllRoutestRequestSerializer,
                                     GetRouteStatusesRequestSerializer,
                                     RouteSerializer, RouteStatusSerializer,
                                     GetChannelDescriptorsRequestSerializer,
                                     PointSerializer,
                                     GetPositionRequestSerializer)
from zeep.cache import InMemoryCache
from zeep.transports import Transport

session = Session()
session.auth = HTTPBasicAuth(settings.NAV_USER, settings.NAV_PASS)

soap_client = zeep.Client(settings.NAV_HOST,
                          transport=Transport(session=session,
                                              cache=InMemoryCache()))


class RawViewSet(viewsets.ViewSet):
    content_negotiation_class = IgnoreClientContentNegotiation

    @action(detail=False)
    @swagger_auto_schema(responses={
        200: DeviceSerializer(many=True,
                              help_text="Структура, содержащая данные по автомобилю")})
    def getAllDevices(self, request):
        """
        Метод возвращает список автомобилей компании, к которой принадлежит пользователь, осуществляющий запрос
        """

        soap_res = soap_client.service.getAllDevices()
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

        soap_res = soap_client.service.getAllDrivers()
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

        soap_res = soap_client.service.getAllDeviceGroups()
        serializer = DeviceGroupSerializer(soap_res, many=True)
        return Response(serializer.data)

    @action(detail=False)
    @swagger_auto_schema(responses={
        200: GeoZoneSerializer(many=True,
                               help_text="Структура, содержащая данные по геозоне")
    })
    def getAllGeoZones(self, request):
        """
        Метод возвращает список геозон, определенных для компании. Идентификаторы сквозные
        """

        soap_res = soap_client.service.getAllGeoZones()
        serializer = GeoZoneSerializer(soap_res, many=True)
        return Response(serializer.data)

    @action(detail=False)
    @swagger_auto_schema(
        query_serializer=GetAllRoutestRequestSerializer,
        responses={
            200: RouteSerializer(many=True,
                                 help_text="Структура, описывающая набор данных, характеризующих маршрут")
        })
    def getAllRoutes(self, request):
        """
        Метод позволяет получить данные по всем маршрутам, содержащимся в базе данных системы (в соответствии с правами пользователя) за заданный промежуток времени.
        В ответ метод возвращает множество структур типа Route, описывающих маршруты, начало которых попало в заданный промежуток. Метод возвращает не более 1000 маршрутов.
        В случае ошибки или, если в заданный промежуток времени не попало ни одного маршрута, метод возвращает пустое значение.
        Даты в формате YYYY-MM-DDTHH:MM:SS
        """

        soap_res = soap_client.service.getAllRoutes(
            request.query_params['ffrom'], request.query_params['to'])
        serializer = RouteSerializer(soap_res, many=True)
        return Response(serializer.data)

    @action(detail=False)
    @swagger_auto_schema(
        query_serializer=GetRouteStatusesRequestSerializer,
        responses={
            200: RouteStatusSerializer(many=True,
                                       help_text="Структура, описывающая статус прохождения маршрута")
        })
    def getRouteStatuses(self, request):
        """
        Методу передается список идентификаторов маршрутов. В ответ метод возвращает список структур RouteStatus, содержащих статусы прохождения всех запрошенных маршрутов.
        В случае ошибки метод возвращает пустое значение
        """

        soap_res = soap_client.service.getRouteStatuses(
            [int(x) for x in request.query_params['routeIds'].split(',')])
        serializer = RouteStatusSerializer(soap_res, many=True)
        return Response(serializer.data)

    @action(detail=False)
    @swagger_auto_schema(
        query_serializer=GetChannelDescriptorsRequestSerializer,
        responses={
            200: ChannelDescriptorSerializer(many=True,
                                             help_text="Структура, содержащая данные по каналу")
        })
    def getChannelDescriptors(self, request):
        """
        Метод возвращает список доступных каналов для запроса по данному устройству.
        Идентификаторы сквозные (один и тот же канал возвращается для разных устройств,
        если его запрос по этому устройству возможен)
        """

        soap_res = soap_client.service.getChannelDescriptors(
            request.query_params['device']
        )
        serializer = ChannelDescriptorSerializer(soap_res, many=True)
        return Response(serializer.data)


class DataViewSet(viewsets.ViewSet):
    content_negotiation_class = IgnoreClientContentNegotiation

    @action(detail=False)
    @swagger_auto_schema(
        query_serializer=GetPositionRequestSerializer,
        responses={
            200: PointSerializer(help_text="Структура, содержащая данные"),
            204: 'No Content',
        })
    def getPosition(self, request):
        """

        """

        soap_res = soap_client.service.getFlatTableSimple(
            request.query_params['device'],
            request.query_params['datetime'],
            request.query_params['datetime'],
            10,
            [0, ],
            ['Approximate', ]
        )
        try:
            serializer = PointSerializer(soap_res.rows[0])
            return Response(serializer.data)
        except IndexError:
            return Response(status=204)
