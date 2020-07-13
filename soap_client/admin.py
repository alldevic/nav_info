from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin
from soap_client.models import NavMtId
from soap_client.resources import NavMtIdResource


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class MtIdFilter(InputFilter):
    parameter_name = 'mt_id'
    title = 'Идентификатор МТ'

    def queryset(self, request, queryset):
        if self.value() is not None:
            mt_id = self.value()
            return queryset.filter(mt_id=mt_id)


class NavIdFilter(InputFilter):
    parameter_name = 'nav_id'
    title = 'Идентификатор навигации'

    def queryset(self, request, queryset):
        if self.value() is not None:
            nav_id = self.value()
            return queryset.filter(nav_id=nav_id)


@admin.register(NavMtId)
class NavMtIdAdmin(ImportExportActionModelAdmin):
    resource_class = NavMtIdResource
    list_display = ('name', 'mt_id', 'nav_id')
    list_filter = (MtIdFilter,  NavIdFilter)
    search_fields = ('name',)
