from rest_framework import serializers
from markets.models import Market

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