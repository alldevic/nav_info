from django.db import models
from django.contrib.postgres.fields import ArrayField


class Device(models.Model):
    id = models.CharField("id",
                          max_length=150,
                          blank=True,
                          null=True)

    name = models.CharField("name",
                            max_length=150,
                            blank=True,
                            null=True)

    regNumber = models.CharField("regNumber",
                                 max_length=150,
                                 blank=True,
                                 null=True)

    serialNumber = models.CharField("serialNumber",
                                    max_length=150,
                                    blank=True,
                                    null=True)

    garageNumber = models.CharField("garageNumber",
                                    max_length=150,
                                    blank=True,
                                    null=True)

    phone = models.CharField("phone",
                             max_length=150,
                             blank=True,
                             null=True)

    simNumber = models.CharField("simNumber",
                                 max_length=150,
                                 blank=True,
                                 null=True)

    fuelSort = models.CharField("fuelSort",
                                max_length=150,
                                blank=True,
                                null=True)

    brand = models.CharField("brand",
                             max_length=150,
                             blank=True,
                             null=True)

    description = models.CharField("description",
                                   max_length=150,
                                   blank=True,
                                   null=True)

    groupIds = ArrayField(models.IntegerField("groupIds",
                                              blank=True,
                                              null=True))

    class Meta(object):
        verbose_name = "автомобиль"
        verbose_name_plural = "автомобили"

    def __str__(self):
        return self.reg_number or self.name


class Driver(models.Model):
    id = models.CharField("id",
                          max_length=150,
                          blank=True,
                          null=True)

    fname = models.CharField("fname",
                             max_length=150,
                             blank=True,
                             null=True)

    mname = models.CharField("mname",
                             max_length=150,
                             blank=True,
                             null=True)

    lname = models.CharField("lname",
                             max_length=150,
                             blank=True,
                             null=True)

    licenceNr = models.CharField("licenceNr",
                                 max_length=150,
                                 blank=True,
                                 null=True)

    phone = models.CharField("phone",
                             max_length=150,
                             blank=True,
                             null=True)

    category = models.CharField("category",
                                max_length=150,
                                blank=True,
                                null=True)

    internalNr = models.CharField("internalNr",
                                  max_length=150,
                                  blank=True,
                                  null=True)

    driverCat = models.CharField("driverCat",
                                 max_length=150,
                                 blank=True,
                                 null=True)

    class Meta(object):
        verbose_name = "водитель"
        verbose_name_plural = "водители"

    def __str__(self):
        return f"{self.lname} {self.fname} {self.mname}"
