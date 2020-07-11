from rest_framework import serializers


class DriverSerializer(serializers.Serializer):
    """
    Структура, содержащая данные по водителю.
    """

    id = serializers.IntegerField(label="id",
                                  help_text="Идентификатор водителя")

    fname = serializers.CharField(label="fname",
                                  help_text="Имя водителя",
                                  max_length=250)

    mname = serializers.CharField(label="mname",
                                  help_text="Отчество водителя",
                                  max_length=250)

    lname = serializers.CharField(label="lname",
                                  help_text="Фамилия водителя",
                                  max_length=250)

    licenceNr = serializers.CharField(label="licenceNr",
                                      help_text="Номер лицензии",
                                      max_length=250)

    phone = serializers.CharField(label="phone",
                                  help_text="Телефон",
                                  max_length=250)

    category = serializers.CharField(label="category",
                                     help_text="Тип лицензии",
                                     max_length=250)

    internalNr = serializers.CharField(label="internalNr",
                                       help_text="Внутренний номер",
                                       max_length=250)

    driverCat = serializers.CharField(label="driverCat",
                                      help_text="Категория прав",
                                      max_length=250)

    class Meta:
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


class DeviceSerializer(serializers.Serializer):
    """
    Структура, содержащая данные по автомобилю.
    """

    id = serializers.IntegerField(label="id",
                                  help_text="Идентификатор устройства слежения")

    name = serializers.CharField(label="name",
                                 help_text="Текстовое наименование устройства (ТС)",
                                 max_length=250)

    regNumber = serializers.CharField(label="regNumber",
                                      help_text="Государственный номер",
                                      max_length=250)

    serialNumber = serializers.CharField(label="serialNumber",
                                         help_text="Серийный номер",
                                         max_length=250)

    garageNumber = serializers.CharField(label="garageNumber",
                                         help_text="Гаражный номер",
                                         max_length=250)

    phone = serializers.CharField(label="phone",
                                  help_text="Телефон",
                                  max_length=250)

    simNumber = serializers.CharField(label="simNumber",
                                      help_text="Номер SIM-карты",
                                      max_length=250)

    fuelSort = serializers.CharField(label="fuelSort",
                                     help_text="Тип топлива",
                                     max_length=250)

    brand = serializers.CharField(label="brand",
                                  help_text="Марка автомобиля",
                                  max_length=250)

    description = serializers.CharField(label="description",
                                        help_text="Текстовое описание устройства (ТС)",
                                        max_length=250)

    groupIds = serializers.ListField(serializers.IntegerField(label="groupId",
                                                              help_text="ID группы",
                                                              allow_null=True),
                                     label="groupIds",
                                     help_text="Список ID групп (клиентов), к которым относится ТС")

    class Meta:
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


class DeviceGroupSerializer(serializers.Serializer):
    """
    Структура содержит данные по группе (клиенту)
    """

    id = serializers.IntegerField(label="id",
                                  help_text="Уникальный идентификатор группы")

    name = serializers.CharField(label="name",
                                 help_text="Имя группы",
                                 max_length=250)

    description = serializers.CharField(label="description",
                                        help_text="Описание группы",
                                        max_length=250)

    parentId = serializers.IntegerField(label="parentId",
                                        help_text="id родительской группы (необязательный параметр)",
                                        allow_null=True,
                                        required=False)

    class Meta:
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

    id = serializers.IntegerField(label="id",
                                  help_text="Идентификатор геозоны")

    name = serializers.CharField(label="name",
                                 max_length=250,
                                 allow_blank=True,
                                 help_text="Текстовое описание")

    points = PointSerializer(label="points",
                             many=True,
                             help_text="Координаты полигона геозоны")

    class Meta:
        fields = (
            "id",
            "name",
            "points",
        )
