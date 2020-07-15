from import_export.fields import Field
from import_export import resources
from soap_client.models import NavMtId


class NavMtIdResource(resources.ModelResource):
    id = Field(attribute='id', column_name='id')
    name = Field(attribute='name', column_name='adres')
    nav_id = Field(attribute='nav_id', column_name='idglosav')
    mt_id = Field(attribute='mt_id', column_name='id')

    def skip_row(self, instance, original):
        try:
            int(instance.nav_id)
        except:
            return True
        return super().skip_row(instance, original)

    class Meta:
        model = NavMtId
        skip_unchanged = True
        report_skipped = False
