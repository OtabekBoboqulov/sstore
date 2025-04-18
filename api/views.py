from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import MarketSerializer
from markets.models import Market, CustomToken
import uuid


@api_view(['POST'])
def signup(request):
    serializer = MarketSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # Creates Market with hashed password
        token = CustomToken.objects.create(market=user, key=str(uuid.uuid4()))
        return Response({'token': token.key, 'market': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('market_username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user and isinstance(user, Market):
        token, _ = CustomToken.objects.get_or_create(
            market=user,
            defaults={'key': str(uuid.uuid4())}
        )
        serializer = MarketSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)