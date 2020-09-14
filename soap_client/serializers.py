from rest_framework import serializers
import pytz


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
                                                              help_text="ID группы"),

                                     label="groupIds",
                                     allow_empty=True,
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


class RouteControlPointSerializer(serializers.Serializer):
    """
    Структура, описывающая контрольные точки маршрута
    """

    geoZoneId = serializers.IntegerField(label="geoZoneId",
                                         help_text="Уникальный идентификатор контрольной точки (геозоны) маршрута")

    ffrom = serializers.DateTimeField(label='from',
                                      source='from',
                                      help_text="Дата и время планового въезда в контрольной точки",
                                      format='%Y-%m-%dT%H:%M:%S',
                                      input_formats=['%Y-%m-%dT%H:%M:%S'],
                                      default_timezone=pytz.utc)

    to = serializers.DateTimeField(label='to',
                                   help_text="Дата и время планового выезда из контрольной точки",
                                   format='%Y-%m-%dT%H:%M:%S',
                                   input_formats=['%Y-%m-%dT%H:%M:%S'],
                                   default_timezone=pytz.utc)

    description = serializers.CharField(label="description",
                                        help_text="Описание контрольной точки маршрута",
                                        max_length=250)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['from'] = rep.pop('ffrom')
        return rep

    class Meta:
        fields = ("geoZoneId",
                  'from',
                  'to',
                  'description',
                  )


# class RouteCriteriumSerializer(serializers.Serializer):


#     class Meta:
#         fields = (
#             'routeCriteriumType',
#             'routeCriteriumValues',
#             'isStatusEffect'
#         )


class RouteSerializer(serializers.Serializer):
    """
    Структура, описывающая набор данных, характеризующих маршрут
    """

    id = serializers.IntegerField(label="id",
                                  help_text="Уникальный идентификатор маршрута")

    name = serializers.CharField(label="name",
                                 max_length=250,
                                 allow_blank=True,
                                 help_text="Имя и описание маршрута")

    ffrom = serializers.DateTimeField(label='from',
                                      source='from',
                                      help_text="Дата и время начала маршрута",
                                      format='%Y-%m-%dT%H:%M:%S',
                                      input_formats=['%Y-%m-%dT%H:%M:%S'],
                                      default_timezone=pytz.utc)

    to = serializers.DateTimeField(label='to',
                                   help_text="Дата и время окончания маршрута",
                                   format='%Y-%m-%dT%H:%M:%S',
                                   input_formats=['%Y-%m-%dT%H:%M:%S'],
                                   default_timezone=pytz.utc)

    planBegin = serializers.DateTimeField(label='planBegin',
                                          help_text="Плановое время начала маршрута",
                                          format='%Y-%m-%dT%H:%M:%S',
                                          input_formats=['%Y-%m-%dT%H:%M:%S'],
                                          default_timezone=pytz.utc)

    planEnd = serializers.DateTimeField(label='planEnd',
                                        help_text="Плановое время окончания маршрута",
                                        format='%Y-%m-%dT%H:%M:%S',
                                        input_formats=['%Y-%m-%dT%H:%M:%S'],
                                        default_timezone=pytz.utc)

    deviceId = serializers.IntegerField(label="deviceId",
                                        help_text='Идентификатор устройства "выполняющего" маршрут')

    driverId = serializers.IntegerField(label="driverId",
                                        help_text='Идентификатор водителя выполняющего маршрут')

    routeControlPoints = RouteControlPointSerializer(label='routeControlPoints',
                                                     help_text="Cписок структур контрольных точек маршрута",
                                                     many=True)
    # routeCriteriums = RouteCriteriumSerializer(label='routeCriteriums',
    #                                            help_text="Список структур критериев оценки прохождения маршрута",
    #                                            many=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['from'] = rep.pop('ffrom')
        return rep

    class Meta:
        fields = ("id",
                  'name',
                  'from',
                  'to',
                  'deviceId',
                  'driverId',
                  'routeControlPoints',
                  #   'routeCriteriums',
                  )


class GetAllRoutestRequestSerializer(serializers.Serializer):
    ffrom = serializers.DateTimeField(label='from',
                                      source='from',
                                      help_text="Дата и время начала маршрута",
                                      format='%Y-%m-%dT%H:%M:%S',
                                      input_formats=['%Y-%m-%dT%H:%M:%S'],
                                      default_timezone=pytz.utc)

    to = serializers.DateTimeField(label='to',
                                   help_text="Дата и время окончания маршрута",
                                   format='%Y-%m-%dT%H:%M:%S',
                                   input_formats=['%Y-%m-%dT%H:%M:%S'],
                                   default_timezone=pytz.utc)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['from'] = rep.pop('ffrom')
        return rep

    class Meta:
        fields = ('from', 'to')


class GetRouteStatusesRequestSerializer(serializers.Serializer):
    routeIds = serializers.ListField(label="routeIDs",
                                     help_text='Cписок идентификаторов маршрутов',
                                     allow_empty=False,
                                     child=serializers.IntegerField())

    class Meta:
        fields = (
            'routeIds',
        )


class ControlPointStatusSerializer(serializers.Serializer):
    """
    Структура, описывающая статус прохождения отдельной контрольной точки (геозоны) маршрута.
    Примечание: для отображения статусов прохождения контрольных точке используется элементы перечисления RouteStatusValue, аналогично статусам маршрутов в целом
    """

    controlPointID = serializers.IntegerField(label="controlPointID",
                                              help_text="Порядковый номер контрольной точки в маршруте")

    controlPointStatusValue = serializers.ChoiceField(label='controlPointStatusValue',
                                                      choices=[
                                                          'Executed', 'NotExecuted', 'ExecutedPartially', 'Performed'],
                                                      help_text='Значение статуса прохождения контрольной точки: выполнен (Executed), не выполнен (NotExecuted), частично выполнен(ExecutedPartially), выполняется(Performed)')

    enterFact = serializers.DateTimeField(label='enterFact',
                                          help_text="Фактическое время входа в контрольную точку",
                                          format='%Y-%m-%dT%H:%M:%S',
                                          input_formats=['%Y-%m-%dT%H:%M:%S'],
                                          default_timezone=pytz.utc)

    exitFact = serializers.DateTimeField(label='exitFact',
                                         help_text="Фактическое время выхода из контрольной точки",
                                         format='%Y-%m-%dT%H:%M:%S',
                                         input_formats=['%Y-%m-%dT%H:%M:%S'],
                                         default_timezone=pytz.utc)

    class Meta:
        fields = (
            'controlPointId',
            'controlPointStatusValue',
            'enterFact',
            'exitFact',
        )


class RouteStatusSerializer(serializers.Serializer):
    """
    Структура, описывающая статус прохождения маршрута.
    Примечание: для описания значений статуса прохождения маршрута используются элементы перечисления RouteStatusValue
    Примечание: для описания статусов прохождения отдельных точек маршрута используется структура ControlPointStatus
    """

    routeId = serializers.IntegerField(label="routeId",
                                       help_text="Уникальный идентификатор маршрута, для которого приводится описание статуса")

    routeStatusValue = serializers.ChoiceField(label='routeStatusValue',
                                               choices=[
                                                   'Executed', 'NotExecuted', 'ExecutedPartially', 'Performed'],
                                               help_text='Значение статуса прохождения маршрута: выполнен (Executed), не выполнен (NotExecuted), частично выполнен(ExecutedPartially), выполняется(Performed)')

    routePercentage = serializers.IntegerField(label="routePercentage",
                                               help_text="Процент прохождения маршрута")

    fromFact = serializers.DateTimeField(label='fromFact',
                                         help_text="Фактическое время начала маршрута",
                                         format='%Y-%m-%dT%H:%M:%S',
                                         input_formats=['%Y-%m-%dT%H:%M:%S'],
                                         default_timezone=pytz.utc)

    toFact = serializers.DateTimeField(label='toFact',
                                       help_text="фактическое время окончания маршрута",
                                       format='%Y-%m-%dT%H:%M:%S',
                                       input_formats=['%Y-%m-%dT%H:%M:%S'],
                                       default_timezone=pytz.utc)

    mileage = serializers.FloatField(label="mileage",
                                     help_text="Пробег по маршруту")

    controlPointStatuses = ControlPointStatusSerializer(label='controlPointStatuses',
                                                        help_text='Статусы прохождения отдельных точек маршрута',
                                                        many=True)

    class Meta:
        fields = (
            'routeId',
            'routeStatusValue',
            'routePercentage',
            'fromFact',
            'tofact',
            'mileage',
            'controlPointStatuses'
        )


class GetChannelDescriptorsRequestSerializer(serializers.Serializer):
    device = serializers.IntegerField(label="device",
                                      help_text='Идентификатор автомобиля',
                                      )

    class Meta:
        fields = (
            'device',
        )


class ChannelDescriptorSerializer(serializers.Serializer):
    """
    Структура, содержащая данные по каналу
    """

    id = serializers.IntegerField(label="id",
                                  help_text="Идентификатор канала")

    name = serializers.CharField(label="name",
                                 max_length=250,
                                 allow_blank=True,
                                 help_text="Имя канала")

    type = serializers.ChoiceField(label='type',
                                   choices=[
                                       'Float', 'Boolean', 'Long', 'Datetime', 'String', 'Point', 'LongSeq'],
                                   help_text='Типы значений каналов')

    class Meta:
        fields = (
            'id',
            'name',
            'type',
        )


class GetPositionRequestSerializer(serializers.Serializer):
    device = serializers.IntegerField(label="device",
                                      help_text="Идентификатор транспортного средства")

    datetime = serializers.DateTimeField(label='datetime',
                                         help_text="Дата в формате YYYY-MM-DDTHH:MM:SS",
                                         format='%Y-%m-%dT%H:%M:%S',
                                         input_formats=['%Y-%m-%dT%H:%M:%S'],
                                         default_timezone=pytz.utc)

    threshold = serializers.IntegerField(label='threshold',
                                         help_text='Погрешность в секундах. Значение вычисляется на отрезке [datetime-threshold; datetime+threshold]',
                                         default=0)

    class Meta:
        fields = (
            'device',
            'datetime',
            'threshold'
        )


class GetCurrentRoutesRequestSerializer(serializers.Serializer):
    time_in = serializers.DateTimeField(label='time_in',
                                        help_text="Дата и время начала маршрута",
                                        format='%Y-%m-%dT%H:%M:%S',
                                        input_formats=['%Y-%m-%dT%H:%M:%S'],
                                        default_timezone=pytz.utc)

    time_out = serializers.DateTimeField(label='time_out',
                                         help_text="Дата и время окончания маршрута",
                                         format='%Y-%m-%dT%H:%M:%S',
                                         input_formats=['%Y-%m-%dT%H:%M:%S'],
                                         default_timezone=pytz.utc)

    class Meta:
        fields = (
            'time_in',
            'time_out'
        )


class MtGeoZoneSerializer(serializers.Serializer):
    description = serializers.CharField(label="description",
                                        help_text="Описание площадки",
                                        max_length=250)

    nav_id = serializers.IntegerField(label="nav_id",
                                      help_text="Идентификатор канала")

    mt_id = serializers.IntegerField(label="mt_id",
                                     help_text="Идентификатор водителя")
    in_time = serializers.CharField(label="in_time",
                                    help_text="Время входа",
                                    max_length=250)
    out_time = serializers.CharField(label="out_time",
                                     help_text="Время выхода",
                                     max_length=250)

    class Meta:
        fields = (
            'description',
            'nav_id',
            'in_time',
            'out_time',
            'mt_id',
        )


class CurrentRoutesSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="id",
                                  help_text="Идентификатор маршрута")
    device = serializers.IntegerField(label="device",
                                      help_text="Идентификатор канала")
    mtIds = serializers.ListField(child=MtGeoZoneSerializer(label="mtId",
                                                            help_text="МТ ID площадки"),

                                  label="mtIds",
                                  allow_empty=True,
                                  help_text="Список МТ ID площадок")

    class Meta:
        fields = (
            'id',
            'device',
            'mtIds',
        )


class GetRouteUnloadsRequestSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(label="id",
                                                               help_text="Идентификатор маршрута"),
                                help_text="Идентификаторы маршрутов",
                                label='ids')

    time_in = serializers.DateTimeField(label='time_in',
                                        help_text="Дата и время начала маршрута",
                                        format='%Y-%m-%dT%H:%M:%S',
                                        input_formats=['%Y-%m-%dT%H:%M:%S'],
                                        default_timezone=pytz.utc)

    time_out = serializers.DateTimeField(label='time_out',
                                         help_text="Дата и время окончания маршрута",
                                         format='%Y-%m-%dT%H:%M:%S',
                                         input_formats=['%Y-%m-%dT%H:%M:%S'],
                                         default_timezone=pytz.utc)

    statuses = serializers.ListField(label='statuses',
                                     help_text="Состояния площадок",
                                     required=False,
                                     allow_empty=False,
                                     child=serializers.ChoiceField(label='statuses',
                                                                   required=False,
                                                                   allow_blank=False,
                                                                   choices=[
                                                                       'Executed', 'NotExecuted', 'ExecutedPartially', 'Performed'],
                                                                   help_text='Значение статуса прохождения контрольной точки: выполнен (Executed), не выполнен (NotExecuted), частично выполнен (ExecutedPartially), выполняется (Performed)'))

    class Meta:
        fields = (
            'ids',
            'time_in',
            'time_out',
            'statuses',
        )


class RouteUnloadsSerializer(serializers.Serializer):
    description = serializers.CharField(label="description",
                                        help_text="Описание площадки",
                                        max_length=250)

    nav_id = serializers.IntegerField(label="nav_id",
                                      help_text="Идентификатор канала")

    mt_id = serializers.IntegerField(label="mt_id",
                                     help_text="Идентификатор водителя")
    in_time = serializers.CharField(label="in_time",
                                    help_text="Время входа",
                                    max_length=250)
    out_time = serializers.CharField(label="out_time",
                                     help_text="Время выхода",
                                     max_length=250)
    state = serializers.CharField(label="state",
                                  help_text="Статус",
                                  max_length=250)

    class Meta:
        fields = (
            'description',
            'nav_id',
            'in_time',
            'out_time',
            'mt_id',
            'state',
        )


class RouteUnloadsSerializerQwe(serializers.Serializer):
    id = serializers.IntegerField(label="id",
                                  help_text="Идентификатор маршрута")
    unloaded_platforms = serializers.ListField(label='unloaded_platforms',
                                               help_text="Состояния площадок",
                                               child=RouteUnloadsSerializer(label='unloaded_platform',
                                                                            help_text='Отгруженная площадка'))

    class Meta:
        fields = (
            'id',
            'unloaded_platforms',
        )
