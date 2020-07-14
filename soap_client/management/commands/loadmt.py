
from django.core.management.base import BaseCommand

from soap_client.resources import NavMtIdResource
import tablib
from django.utils import timezone


class Command(BaseCommand):
    help = 'Удаление локальных данных'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        begin_time = timezone.now()
        self.stdout.write(self.style.SUCCESS(f'BEGIN AT {begin_time}'))

        try:
            with open(options['file'], 'rb') as fh:
                dataset = tablib.Dataset().load(fh)
                rsc = NavMtIdResource()
                rsc.import_data(dataset, dry_run=False)
        except Exception as err:
            self.stdout.write(self.style.ERROR(err))
        finally:
            end_time = timezone.now()
            self.stdout.write(self.style.SUCCESS(f'END AT: {end_time}'))
            self.stdout.write(self.style.SUCCESS(
                f'ESTIMATED: {end_time - begin_time}'))
