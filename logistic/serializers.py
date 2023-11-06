from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе

    # product = serializers.PrimaryKeyRelatedField(
    #     queryset=Product.objects.all(),
    # )

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    # настройте сериализатор для склада

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)
        for position in positions:
            StockProduct(
                stock=stock,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price']
            ).save()
        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)
        instance.positions.all().delete()
        for position in positions:
            StockProduct(
                stock=stock,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price']
            ).save()

        return stock
