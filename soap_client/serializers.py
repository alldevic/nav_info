from rest_framework import serializers
from soap_client.models import (Driver, Device)


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
