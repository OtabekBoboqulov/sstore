from rest_framework import serializers
from markets.models import Market
from products.models import Product, Category


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
    class Meta:
        model = Product
        fields = ['id', 'category_id', 'name', 'quantity', 'quantity_type', 'price_per_quantity', 'status', 'date']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'market_id', 'date']
