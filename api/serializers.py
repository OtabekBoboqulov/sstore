from rest_framework import serializers
from markets.models import Market


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ['id', 'market_username', 'market_name', 'phone_number', 'profile_picture', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Market.objects.create(
            market_username=validated_data['market_username'],
            market_name=validated_data.get('market_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
