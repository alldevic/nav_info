from rest_framework import serializers
from soap_client.models import (Driver, Device, DeviceGroup, Point, GeoZone)


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = (
            'id',
            'fname',
            'mname',
            'lname',
            'licenceNr',
            'phone',
            'category',
            'internalNr',
            'driverCat',
        )


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'id',
            'name',
            'regNumber',
            'serialNumber',
            'garageNumber',
            'phone',
            'simNumber',
            'fuelSort',
            'brand',
            'description',
            'groupIds',
        )


class DeviceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceGroup
        fields = (
            'id',
            'name',
            'description',
            'parentId',
        )


class PointSerializer(serializers.Serializer):
    """
    Широта и долгота (координата)
    """

    lat = serializers.FloatField(label="lat",
                                 help_text="Широта")

    lon = serializers.FloatField(label="lon",
                                 help_text="Долгота")

    class Meta:
        fields = (
            "lat",
            "lon",
        )


class GeoZoneSerializer(serializers.Serializer):
    """
    Структура, содержащая данные по геозоне
    """

    id = serializers.IntegerField(help_text="Идентификатор геозоны")

    name = serializers.CharField(max_length=250,
                                 allow_blank=True,
                                 help_text="Текстовое описание")

    points = PointSerializer(many=True,
                             help_text="Координаты полигона геозоны")

    class Meta:
        fields = (
            "id",
            "name",
            "points",
        )
