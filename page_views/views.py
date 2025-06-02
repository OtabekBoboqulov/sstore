import cloudinary.uploader
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Case, When, IntegerField
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse
from api.serializers import ProductSerializer, CategorySerializer, ProductUpdateSerializer, ExpanseSerializer, \
    MarketSerializer
from api.authentication import CustomTokenAuthentication
from products.models import Product, Category, ProductUpdate
from reports.models import Expanse
from io import BytesIO
from openpyxl.utils import get_column_letter
import pandas as pd


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
    current_month_text = datetime.now().strftime('%B')
    current_day = datetime.now().day
    start_date = timezone.make_aware(datetime(datetime.now().year, current_month, 1))
    profit = list()
    market_data = request.user
    market_serialized = MarketSerializer(market_data)
    for i in range(1, current_day + 1):
        end_date = timezone.make_aware(datetime(datetime.now().year, current_month, i, 23, 59, 59, 999999))
        updates = ProductUpdate.objects.all().filter(product_id__in=product_ids, status='subed', date__gte=start_date,
                                                     date__lte=end_date)
        updates_added = ProductUpdate.objects.all().filter(product_id__in=product_ids, status='added',
                                                           date__gte=start_date, date__lte=end_date)
        updates_serialized = ProductUpdateSerializer(updates, many=True)
        updates_added_serialized = ProductUpdateSerializer(updates_added, many=True)
        profit_from_sells = sum(list(map(float, [update['price'] for update in updates_serialized.data])))
        expanse_from_products = sum(list(map(float, [update['price'] for update in updates_added_serialized.data])))
        expanses = Expanse.objects.all().filter(market_id=request.user.id, date__gte=start_date, date__lte=end_date)
        expanses_serialized = ExpanseSerializer(expanses, many=True)
        expanses_sum = sum(list(map(float, [expanse['price'] for expanse in expanses_serialized.data])))
        profit.append(profit_from_sells - expanse_from_products - expanses_sum)
    try:
        income = profit_from_sells
        expanses_total = expanses_sum + expanse_from_products
        products_added = sum(list(map(int, [update['quantity'] for update in updates_added_serialized.data])))
        products_subbed = sum(list(map(int, [update['quantity'] for update in updates_serialized.data])))
    except NameError:
        income, expanses_total, products_subbed, products_added = 0, 0, 0, 0
    products_ordered_by_sells = order_products_by_sells(markets)
    products_serialized_by_sells = ProductSerializer(products_ordered_by_sells, many=True)
    products_ordered_by_price = order_products_by_price(markets)
    products_serialized_by_price = ProductSerializer(products_ordered_by_price, many=True)
    quantity = sum([product["quantity"] for product in products_serialized.data])
    return Response([{'products': products_serialized.data}] + [{'quantity': quantity}] + [
        {'products_by_sells': products_serialized_by_sells.data}] + [
                        {'products_by_price': products_serialized_by_price.data}] + [{'profit': profit}] + [
                        {'market_data': market_serialized.data}] + [{'income': income}] + [
                        {'expanses_total': expanses_total}] + [{'products_subbed': products_subbed}] + [
                        {'products_added': products_added}] + [{'current_month': current_month_text}])


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def categories(request):
    categories = Category.objects.all().filter(market_id=request.user.id)
    category_serialized = CategorySerializer(categories, many=True)
    return Response(category_serialized.data)


@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def category_create(request):
    try:
        category = Category(name=request.data['name'], market_id=request.user)
        category.save()
        return Response({'message': 'Category created successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def products(request):
    categories = Category.objects.all().filter(market_id=request.user.id)
    category_serialized = CategorySerializer(categories, many=True)
    markets = [category['id'] for category in category_serialized.data if category['market_id'] == request.user.id]
    products = Product.objects.all().filter(category_id__in=markets)
    products_serialized = ProductSerializer(products, many=True)
    products_quantity = len(products_serialized.data)
    available_products = len([product for product in products_serialized.data if product['status'] == 'available'])
    few_products = len([product for product in products_serialized.data if product['status'] == 'few'])
    ended_products = len([product for product in products_serialized.data if product['status'] == 'ended'])
    return Response({'products': products_serialized.data, 'products_quantity': products_quantity,
                     'available_products': available_products, 'few_products': few_products,
                     'ended_products': ended_products})


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def product_edit(request, pk):
    product = Product.objects.get(id=pk)
    product_serialized = ProductSerializer(product)
    return Response(product_serialized.data)


@api_view(['PUT'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def product_update(request, pk):
    category = Category.objects.get(id=request.data['category_id'])
    product = Product.objects.get(id=pk)
    if 'image' in request.FILES:
        file = request.FILES['image']
        result = cloudinary.uploader.upload(file)
    else:
        result = {'public_id': 'sstore_products/0c32b31941863a0f1fb8e97eaf55f595_lc10im'}
    request.data._mutable = True
    request.data['image'] = result['public_id']
    request.data._mutable = False
    product_serialized = ProductSerializer(product, data=request.data)
    if product_serialized.is_valid():
        product_serialized.validated_data['category_id'] = category
        product_serialized.save()
        return Response({'message': 'Product updated successfully'})
    return Response(product_serialized.errors, status=400)


@api_view(['DELETE'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def product_delete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return Response({'message': 'Product deleted successfully'})


@api_view(['DELETE'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def product_delete_several(request):
    ids = request.data['ids']
    Product.objects.filter(id__in=ids).delete()
    return Response({'message': 'Products deleted successfully'})


@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def product_create(request):
    try:
        category = Category.objects.get(id=request.data['category_id'])
        if 'image' in request.FILES:
            file = request.FILES['image']
            result = cloudinary.uploader.upload(file)
        else:
            result = {'public_id': 'sstore_products/0c32b31941863a0f1fb8e97eaf55f595_lc10im'}
        product = Product(category_id=category, name=request.data['name'], quantity=request.data['quantity'],
                          quantity_type=request.data['quantity_type'],
                          price_per_quantity=request.data['price_per_quantity'], image=result['public_id'],
                          status='available')
        product.save()
        return Response({'message': 'Product created successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def products_report(request):
    categories = Category.objects.all().filter(market_id=request.user.id)
    category_serialized = CategorySerializer(categories, many=True)
    markets = [category['id'] for category in category_serialized.data if category['market_id'] == request.user.id]
    products = Product.objects.all().filter(category_id__in=markets)
    products_serialized = ProductSerializer(products, many=True)
    data = {
        'Mahsulot nomi': [product['name'] for product in products_serialized.data],
        'Kategoriya': [product['category_name'] for product in products_serialized.data],
        'Qoldiq': [product['quantity'] for product in products_serialized.data],
        'Status': [product['status'] for product in products_serialized.data],
        'Narx': [product['price_per_quantity'] for product in products_serialized.data]
    }
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        worksheet = writer.sheets['Sheet1']
        for column in range(1, len(data) + 1):
            max_length = max(
                len(str(df.iloc[:, column - 1].values[i]))
                for i in range(len(df)) if df.iloc[:, column - 1].values[i]
            ) + 2
            adjusted_width = min(max_length, 50)
            worksheet.column_dimensions[get_column_letter(column)].width = adjusted_width
    output.seek(0)
    response = HttpResponse(
        content=output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=products_report.xlsx'
    return response

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
#
# def trigger_dashboard_update(user_id):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         f"dashboard_{user_id}",
#         {
#             "type": "dashboard_update"
#         }
#     )
