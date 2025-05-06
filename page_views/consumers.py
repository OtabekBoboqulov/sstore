from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from products.models import Category, Product, ProductUpdate
from reports.models import Expanse
from api.serializers import CategorySerializer, ProductSerializer, ProductUpdateSerializer, ExpanseSerializer, \
    MarketSerializer
from .views import order_products_by_price, order_products_by_sells
from markets.models import Market
from datetime import datetime
from django.utils import timezone
import json


# Synchronous function to gather dashboard data
@sync_to_async
def get_dashboard_data(market_id, market_instance):
    now = datetime.now()
    start_date = timezone.make_aware(datetime(now.year, now.month, 1))
    current_day = now.day
    end_of_month = timezone.make_aware(datetime(now.year, now.month, current_day, 23, 59, 59, 999999))

    # Database queries
    categories = Category.objects.filter(market_id=market_id)
    category_ids = categories.values_list("id", flat=True)
    products = Product.objects.filter(category_id__in=category_ids)
    product_ids = products.values_list("id", flat=True)

    # Calculate daily profit
    profit = []
    for i in range(1, current_day + 1):
        end_date = timezone.make_aware(datetime(now.year, now.month, i, 23, 59, 59, 999999))
        updates = ProductUpdate.objects.filter(
            product_id__in=product_ids, status="subed", date__range=(start_date, end_date)
        )
        updates_added = ProductUpdate.objects.filter(
            product_id__in=product_ids, status="added", date__range=(start_date, end_date)
        )
        expanses = Expanse.objects.filter(market_id=market_id, date__range=(start_date, end_date))
        profit_sells = sum(float(u.price) for u in updates)
        expanse_products = sum(float(u.price) for u in updates_added)
        expanse_total = sum(float(e.price) for e in expanses)
        profit.append(profit_sells - expanse_products - expanse_total)

    # Aggregate data for the entire month
    all_updates = ProductUpdate.objects.filter(
        product_id__in=product_ids, status="subed", date__range=(start_date, end_of_month)
    )
    all_updates_added = ProductUpdate.objects.filter(
        product_id__in=product_ids, status="added", date__range=(start_date, end_of_month)
    )
    all_expanses = Expanse.objects.filter(market_id=market_id, date__range=(start_date, end_of_month))

    # Serialization
    updates_serialized = ProductUpdateSerializer(all_updates, many=True).data
    updates_added_serialized = ProductUpdateSerializer(all_updates_added, many=True).data
    products_serialized = ProductSerializer(products, many=True).data
    market_serialized = MarketSerializer(market_instance).data

    # Prepare response data
    response_data = {
        "products": products_serialized,
        "quantity": sum(p["quantity"] for p in products_serialized),
        "products_by_sells": ProductSerializer(order_products_by_sells(category_ids), many=True).data,
        "products_by_price": ProductSerializer(order_products_by_price(category_ids), many=True).data,
        "profit": profit,
        "market_data": market_serialized,
        "income": sum(float(u["price"]) for u in updates_serialized),
        "expanses_total": sum(float(e.price) for e in all_expanses),
        "products_subbed": sum(int(u["quantity"]) for u in updates_serialized),
        "products_added": sum(int(u["quantity"]) for u in updates_added_serialized),
        "current_month": now.strftime("%B"),
    }
    return response_data


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.market_id = self.scope['user'].id
        self.group_name = f"dashboard_{self.market_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_dashboard_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_dashboard_data(self):
        data = await get_dashboard_data(self.market_id, self.scope['user'])
        await self.send(text_data=json.dumps(data))

    async def dashboard_update(self, event):
        await self.send_dashboard_data()
