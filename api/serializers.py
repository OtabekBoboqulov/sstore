from rest_framework import serializers
from markets.models import Market
from products.models import Product, Category, ProductUpdate
from reports.models import Expanse


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ['id', 'phone_number', 'market_name', 'profile_picture', 'password', 'plan']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Market.objects.create(
            phone_number=validated_data['phone_number'],
            market_name=validated_data.get('market_name', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProductSerializer(serializers.ModelSerializer):
    total_subtracted = serializers.IntegerField(required=False, read_only=True)
    total_sold_price = serializers.IntegerField(required=False, read_only=True)
    category_name = serializers.CharField(source='category_id.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category_name', 'name', 'quantity', 'quantity_type', 'price_per_quantity', 'image',
                  'status', 'date', 'total_subtracted', 'total_sold_price']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'market_id', 'date']


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUpdate
        fields = ['id', 'product_id', 'status', 'quantity', 'price', 'date']


class ExpanseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expanse
        fields = ['id', 'market_id', 'type', 'price', 'date']
