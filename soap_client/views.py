from datetime import datetime, timedelta

import zeep
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from requests import Session
from requests.auth import HTTPBasicAuth
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from zeep.cache import InMemoryCache
from zeep.transports import Transport
from zeep.helpers import serialize_object
from nav_info import settings
from soap_client.models import NavMtId
from soap_client.negotiation import IgnoreClientContentNegotiation
from soap_client.serializers import (ChannelDescriptorSerializer,
                                     CurrentRoutesSerializer,
                                     DeviceGroupSerializer, DeviceSerializer,
                                     DriverSerializer, GeoZoneSerializer,
                                     GetAllRoutestRequestSerializer,
                                     GetChannelDescriptorsRequestSerializer,
                                     GetCurrentRoutesRequestSerializer,
                                     GetPositionRequestSerializer,
                                     GetRouteStatusesRequestSerializer,
                                     PointSerializer, RouteSerializer,
                                     RouteStatusSerializer,
                                     GetRouteUnloadsRequestSerializer,
                                     RouteUnloadsSerializer,
                                     RouteUnloadsSerializerQwe)
import json

session = Session()
session.auth = HTTPBasicAuth(settings.NAV_USER, settings.NAV_PASS)

soap_client = zeep.Client(settings.NAV_HOST,
                          transport=Transport(session=session,
                                              cache=InMemoryCache()))

navmtids = [x for x in NavMtId.objects.all()]


class RawViewSet(viewsets.ViewSet):
    content_negotiation_class = IgnoreClientContentNegotiation

    @action(detail=False)
    @swagger_auto_schema(responses={
        200: DeviceSerializer(many=True,
                              help_text="Структура, содержащая данные по автомобилю")
    })
    @method_decorator(cache_page(settings.CACHE_LONG_TTL))
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
                              help_text="Структура, содержащая данные по водителю")
    })
    @method_decorator(cache_page(settings.CACHE_LONG_TTL))
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
                                   help_text="Структура содержит данные по группе (клиенту)")
    })
    @method_decorator(cache_page(settings.CACHE_LONG_TTL))
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
    @method_decorator(cache_page(settings.CACHE_LONG_TTL))
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
    @method_decorator(cache_page(settings.CACHE_LONG_TTL))
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
            200: PointSerializer(help_text="Широта и долгота (координата)"),
            204: 'No Content',
        })
    def getDevicePosition(self, request):
        """
        Метод, возвращающий позицию устройства в определенный момент времени
        """
        query_dt = request.query_params['datetime']
        query_td = int(request.query_params['threshold'])
        date_from = datetime.strptime(
            query_dt, '%Y-%m-%dT%H:%M:%S') - timedelta(seconds=query_td)
        date_to = datetime.strptime(
            query_dt, '%Y-%m-%dT%H:%M:%S') + timedelta(seconds=query_td)
        soap_res = soap_client.service.getFlatTableSimple(
            int(request.query_params['device']),
            date_from.strftime('%Y-%m-%dT%H:%M:%S'),
            date_to.strftime('%Y-%m-%dT%H:%M:%S'),
            0,
            [0, ],
            ['Approximate', ]
        )
        try:
            serializer = PointSerializer(
                soap_res.rows[0].values[0].pointValue)
            return Response(serializer.data)
        except IndexError:
            return Response(status=204)

    @action(detail=False)
    @swagger_auto_schema(
        query_serializer=GetCurrentRoutesRequestSerializer,
        responses={
            200: CurrentRoutesSerializer(help_text="Текущий марщрут", many=True),
        })
    def getCurrentRoutes(self, request):
        """
        Cегодняшний маршруты, которые необходимо пройти 
        """
        time_in = request.query_params['time_in']
        time_out = request.query_params['time_out']

        all_routes = soap_client.service.getAllRoutes(time_in, time_out)
        all_routes = serialize_object(all_routes)
        res = []
        for route in all_routes:
            res_route = {}
            res_route['id'] = int(route['id'])
            res_route['device'] = int(route['deviceId'])
            mt_ids = []
            for geozone in route['routeControlPoints']:
                geozone_res = {}
                geozone_res["description"] = geozone['description']
                geozone_res["in_time"] = geozone['from']
                geozone_res["out_time"] = geozone['to']
                geozone_res['nav_id'] = int(geozone['geoZoneId'])
                try:
                    geozone_res['mt_id'] = [
                        x for x in navmtids if x.nav_id == geozone_res['nav_id']]
                    geozone_res['mt_id'] = geozone_res['mt_id'][0].mt_id
                except:
                    geozone_res['mt_id'] = -1

                mt_ids.append(geozone_res)
            res_route['mtIds'] = mt_ids
            res.append(res_route)

        serializer = CurrentRoutesSerializer(res, many=True)
        return Response(serializer.data)

    @action(detail=False)
    @swagger_auto_schema(
        query_serializer=GetRouteUnloadsRequestSerializer,
        responses={
            200: RouteUnloadsSerializerQwe(help_text="Текущий марщрут", many=True),
        })
    def getRouteUnloads(self, request):
        # 20278916
        route_ids = [int(x) for x in request.query_params['ids'].split(',')]
        time_in = request.query_params['time_in']
        time_out = request.query_params['time_out']

        soap_res = serialize_object(
            soap_client.service.getRouteStatuses(route_ids))

        all_routes = soap_client.service.getAllRoutes(time_in, time_out)

        res = []
        i = 0
        for route_id in route_ids:
            rt_res = {}
            rt_res['id'] = route_id
            qwe = []
            try:
                route = [x for x in serialize_object(
                    all_routes) if x['id'] == route_id][0]
            except:
                continue

            for status in soap_res[i]['controlPointStatuses']:
                tmp = {}
                tmp['state'] = status['controlPointStatusValue']
                geozone = route['routeControlPoints'][int(
                    status['controlPointID'])]
                tmp['nav_id'] = geozone['geoZoneId']
                try:
                    tmp['mt_id'] = [
                        x for x in navmtids if x.nav_id == tmp['nav_id']]
                    tmp['mt_id'] = tmp['mt_id'][0].mt_id
                except:
                    tmp['mt_id'] = -1
                tmp["in_time"] = geozone['from']
                tmp["out_time"] = geozone['to']
                tmp["description"] = geozone["description"]
                qwe.append(tmp)
            rt_res['unloaded_platforms'] = qwe
            i += 1
            res.append(rt_res)

        serializer = RouteUnloadsSerializerQwe(res, many=True)
        return Response(serializer.data)
