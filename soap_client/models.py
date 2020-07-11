from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid


class Device(models.Model):
    """
    Структура, содержащая данные по автомобилю.
    """

    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)

    id = models.CharField("id",
                          help_text="Идентификатор устройства слежения",
                          max_length=150,
                          blank=True,
                          null=True)

    name = models.CharField("name",
                            help_text="Текстовое наименование устройства (ТС)",
                            max_length=150,
                            blank=True,
                            null=True)

    regNumber = models.CharField("regNumber",
                                 help_text="Государственный номер",
                                 max_length=150,
                                 blank=True,
                                 null=True)

    serialNumber = models.CharField("serialNumber",
                                    help_text="Серийный номер",
                                    max_length=150,
                                    blank=True,
                                    null=True)

    garageNumber = models.CharField("garageNumber",
                                    help_text="Гаражный номер",
                                    max_length=150,
                                    blank=True,
                                    null=True)

    phone = models.CharField("phone",
                             help_text="Телефон",
                             max_length=150,
                             blank=True,
                             null=True)

    simNumber = models.CharField("simNumber",
                                 help_text="Номер SIM-карты",
                                 max_length=150,
                                 blank=True,
                                 null=True)

    fuelSort = models.CharField("fuelSort",
                                help_text="Тип топлива",
                                max_length=150,
                                blank=True,
                                null=True)

    brand = models.CharField("brand",
                             help_text="Марка автомобиля",
                             max_length=150,
                             blank=True,
                             null=True)

    description = models.CharField("description",
                                   help_text="Текстовое описание устройства (ТС)",
                                   max_length=150,
                                   blank=True,
                                   null=True)

    groupIds = ArrayField(models.IntegerField("groupIds",
                                              blank=True,
                                              null=True),
                          help_text="Список ID групп (клиентов), к которым относится ТС",
                          blank=True,
                          null=True)

    class Meta(object):
        verbose_name = "автомобиль"
        verbose_name_plural = "автомобили"

    def __str__(self):
        return self.reg_number or self.name


class Driver(models.Model):
    """
    Структура, содержащая данные по водителю. 
    """

    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)

    id = models.CharField("id",
                          help_text="Идентификатор водителя",
                          max_length=150,
                          blank=True,
                          null=True)

    fname = models.CharField("fname",
                             help_text="Имя водителя",
                             max_length=150,
                             blank=True,
                             null=True)

    mname = models.CharField("mname",
                             help_text="Отчество водителя",
                             max_length=150,
                             blank=True,
                             null=True)

    lname = models.CharField("lname",
                             help_text="Фамилия водителя",
                             max_length=150,
                             blank=True,
                             null=True)

    licenceNr = models.CharField("licenceNr",
                                 help_text="Номер лицензии",
                                 max_length=150,
                                 blank=True,
                                 null=True)

    phone = models.CharField("phone",
                             help_text="Телефон",
                             max_length=150,
                             blank=True,
                             null=True)

    category = models.CharField("category",
                                help_text="Тип лицензии",
                                max_length=150,
                                blank=True,
                                null=True)

    internalNr = models.CharField("internalNr",
                                  help_text="Внутренний номер",
                                  max_length=150,
                                  blank=True,
                                  null=True)

    driverCat = models.CharField("driverCat",
                                 help_text="Категория прав",
                                 max_length=150,
                                 blank=True,
                                 null=True)

    class Meta(object):
        verbose_name = "водитель"
        verbose_name_plural = "водители"

    def __str__(self):
        return f"{self.lname} {self.fname} {self.mname}"
