from django.db import models


class NavMtId(models.Model):
    name = models.CharField("name",
                            help_text="Название из МТ",
                            max_length=250,
                            blank=True,
                            null=True)

    nav_id = models.IntegerField("nav_id",
                                 help_text="Идентификатор навигации")

    mt_id = models.IntegerField("mt_id",
                                help_text="Идентификатор МТ",
                                blank=True,
                                null=True)

    class Meta(object):
        verbose_name = "площадка МТ"
        verbose_name_plural = "площадки МТ"

    def __str__(self):
        return self.name
