from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.serializers import ProductSerializer, CategorySerializer
from api.authentication import CustomTokenAuthentication
from products.models import Product, Category


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def dashboard(request):
    categories = Category.objects.all().filter(market_id=request.user.id)
    category_serialized = CategorySerializer(categories, many=True)
    markets = [category['id'] for category in category_serialized.data if category['market_id'] == request.user.id]
    products = Product.objects.all().filter(category_id__in=markets)
    products_serialized = ProductSerializer(products, many=True)
    quantity = sum([product["quantity"] for product in products_serialized.data])
    print(quantity)
    return Response(products_serialized.data + [{'quantity': quantity}])
