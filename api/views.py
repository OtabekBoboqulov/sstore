from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import MarketSerializer
from markets.models import Market, CustomToken
from .authentication import CustomTokenAuthentication
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
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')

    if not phone_number or not password:
        return Response({'error': 'Phone number and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=phone_number, password=password)
    if user and isinstance(user, Market):
        token, _ = CustomToken.objects.get_or_create(
            market=user,
            defaults={'key': str(uuid.uuid4())}
        )
        serializer = MarketSerializer(user)
        return Response({'token': token.key, 'market': serializer.data})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.custom_tokens.all().delete()
    return Response({'message': 'Successfully logged out'})
