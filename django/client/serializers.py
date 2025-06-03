from client.models import Client, Historical
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"


class HistoricalSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)

    class Meta:
        model = Historical
        fields = ('id', 'client', 'client_name', 'value', 'observation', 'date')
