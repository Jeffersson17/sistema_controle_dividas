from client.models import Client, Historical

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import ClientSerializer, HistoricalSerializer


class RegisterUser(APIView):
    def post(self, request):
        try:
            user = User.objects.create(
                username=request.data['username'],
                email=request.data['email'],
                is_active=True,
                password=make_password(request.data['password'])
            )
            if User.objects.filter(username=request.data['username']).exists():
                return Response({"error": "Usuário já existe"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Usuário criado com sucesso"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class HistoricalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Historical.objects.all().order_by('-id')
    serializer_class = HistoricalSerializer

    @action(detail=False, methods=['get'], url_path='by-client/(?P<client_id>[^/.]+)')
    def get_by_client(self, request, client_id=None):
        historicals = Historical.objects.filter(client_id=client_id).order_by('-date')
        serializer = self.get_serializer(historicals, many=True)
        return Response(serializer.data)

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
