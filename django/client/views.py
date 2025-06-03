from client.models import Client, Historical

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ClientSerializer, HistoricalSerializer


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class HistoricalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Historical.objects.all()
    serializer_class = HistoricalSerializer

    def create(self, request, *args, **kwargs):
        client_id = request.data.get('client')
        value = request.data.get('value')
        observation = request.data.get('observation', '')
        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            return Response(
                {'detail': 'Cliente não encontrado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if float(value) > 0:
            client.increase_debt(value, observation)
        else:
            client.reduce_debt(abs(float(value)), observation)
        hist = client.historicos.order_by('-date').first()
        serializer = self.get_serializer(hist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
