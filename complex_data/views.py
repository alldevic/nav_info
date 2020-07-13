from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from soap_client.negotiation import IgnoreClientContentNegotiation


class DataViewSet(viewsets.ViewSet):
    content_negotiation_class = IgnoreClientContentNegotiation

    @action(detail=False)
    def sayHello(self, request):
        return Response("hello")
