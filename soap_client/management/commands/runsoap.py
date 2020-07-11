import zeep
from django.core.management.base import BaseCommand
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.cache import InMemoryCache
from zeep.transports import Transport
from nav_info import settings


class Command(BaseCommand):
    help = 'Run SOAP navigation client'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        session = Session()
        session.auth = HTTPBasicAuth(settings.NAV_USER, settings.NAV_PASS)

        self.client = zeep.Client(settings.NAV_HOST,
                                  transport=Transport(session=session,
                                                      cache=InMemoryCache()))

    def getAllDevices(self):
        return self.client.service.getAllDevices()

    def getAllDrivers(self):
        return self.client.service.getAllDrivers()

    def getAllGeoZones(self):
        return self.client.service.getAllGeoZones()

    def handle(self, *args, **options):
        print(self.getAllDevices())
