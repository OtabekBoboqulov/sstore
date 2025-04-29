from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Case, When, IntegerField
from datetime import datetime
from django.utils import timezone
from api.serializers import ProductSerializer, CategorySerializer, ProductUpdateSerializer, ExpanseSerializer, \
    MarketSerializer
from api.authentication import CustomTokenAuthentication
from products.models import Product, Category, ProductUpdate
from reports.models import Expanse


def order_products_by_sells(markets):
    return Product.objects.filter(category_id__in=markets).annotate(
        total_subtracted=Sum(
            Case(
                When(updates__status='subed', then='updates__quantity'),
                default=0,
                output_field=IntegerField()
            )
        )
    ).order_by('-total_subtracted')


def order_products_by_price(markets):
    return Product.objects.filter(category_id__in=markets).annotate(
        total_sold_price=Sum(
            Case(
                When(updates__status='subed', then='updates__price'),
                default=0,
                output_field=IntegerField()
            )
        )
    ).order_by('-total_sold_price')


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def dashboard(request):
    categories = Category.objects.all().filter(market_id=request.user.id)
    category_serialized = CategorySerializer(categories, many=True)
    markets = [category['id'] for category in category_serialized.data if category['market_id'] == request.user.id]
    products = Product.objects.all().filter(category_id__in=markets)
    products_serialized = ProductSerializer(products, many=True)
    product_ids = [product['id'] for product in products_serialized.data]
    current_month = datetime.now().month
    current_day = datetime.now().day
    start_date = timezone.make_aware(datetime(datetime.now().year, current_month, 1))
    profit = list()
    market_data = request.user
    market_serialized = MarketSerializer(market_data)
    for i in range(1, current_day + 1):
        end_date = timezone.make_aware(datetime(datetime.now().year, current_month, i, 23, 59, 59, 999999))
        updates = ProductUpdate.objects.all().filter(product_id__in=product_ids, status='subed', date__gte=start_date,
                                                     date__lte=end_date)
        updates_serialized = ProductUpdateSerializer(updates, many=True)
        profit_from_sells = sum(list(map(float, [update['price'] for update in updates_serialized.data])))
        expanses = Expanse.objects.all().filter(market_id=request.user.id, date__gte=start_date, date__lte=end_date)
        expanses_serialized = ExpanseSerializer(expanses, many=True)
        expanses_sum = sum(list(map(float, [expanse['price'] for expanse in expanses_serialized.data])))
        profit.append(profit_from_sells - expanses_sum)
    products_ordered_by_sells = order_products_by_sells(markets)
    products_serialized_by_sells = ProductSerializer(products_ordered_by_sells, many=True)
    products_ordered_by_price = order_products_by_price(markets)
    products_serialized_by_price = ProductSerializer(products_ordered_by_price, many=True)
    quantity = sum([product["quantity"] for product in products_serialized.data])
    return Response([{'products': products_serialized.data}] + [{'quantity': quantity}] + [
        {'products_by_sells': products_serialized_by_sells.data}] + [
                        {'products_by_price': products_serialized_by_price.data}] + [{'profit': profit}] + [
                        {'market_data': market_serialized.data}])
