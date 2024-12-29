import json
from app_modules.orders import models
from .tasks import process_order_items
from rest_framework import serializers
from app_modules.products.models import Products
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from app_modules.orders.signals import MergeExistingItemException
from app_modules.users.serializers import UserBasicDetailsSerializer
from app_modules.products.serializers import ProductBasicDetailsSerializer

class OrderDataSerializer(serializers.ModelSerializer):

    order_product = serializers.SerializerMethodField()
    customer      = serializers.SerializerMethodField()
    created_at    = serializers.DateTimeField(format='%b %d, %Y %I:%M %p')

    class Meta:
        model  = models.Order
        fields = (
            "id",
            "created_at",
            "customer",
            "status",
            "order_product",
            "total_amount",
            "discount",
            "final_amount",
        )

    def get_order_product(self,obj):
        return OrderProductDataSerializer(
            obj.order_items.all(),
            many=True
        ).data
    
    def get_customer(self,obj):
        return UserBasicDetailsSerializer(obj.customer).data

class OrderSerializer(serializers.ModelSerializer):

    order_product = serializers.ListField(required=False)

    class Meta:
        model  = models.Order
        fields = (
            "customer",
            "status",
            "order_product",
        )

    def _get_total_amount(self, order_products):
        return sum((models.Products.objects.get(id=product["id"]).price * product["quantity"]) for product in order_products)

    def create(self, validated_data):
        order_products = validated_data.pop('order_product',[])

        if not order_products:
            raise ValidationError("At least one product is required.")

        order_products = [json.loads(order) for order in order_products]

        for product in order_products:
            order_product_serializer = OrderProductSerializer(data=product)
            order_product_serializer.is_valid(raise_exception=True)

        order_amount= self._get_total_amount(order_products)

        order_obj = models.Order(**validated_data)
        order_obj.total_amount = order_amount
        order_obj.save()

        process_order_items(order_obj.id, order_products)

        return order_obj
        
class OrderProductSerializer(serializers.Serializer):

    id       = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate(self, attrs):

        product_id = attrs.get('id')
        requested_quantity = attrs.get('quantity')

        if product_id is None:
            raise ValidationError("Product ID is required.")
        
        if requested_quantity is None:
            raise ValidationError("Quantity is required.")

        try:
            product = Products.objects.get(id=product_id)
        except ObjectDoesNotExist:
            raise ValidationError(f"Product with ID {product_id} does not exist.")

        if requested_quantity > product.stock:
            raise ValidationError(f"Insufficient stock for product ID {product_id}. Available: {product.stock}, Requested: {requested_quantity}.")

        return super().validate(attrs)

class OrderProductDataSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model  = models.OrderItem
        fields = (
            "id",
            "product",
            "quantity",
            "price",
            "total",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductBasicDetailsSerializer(instance.product).data 
        return representation
    
    def create(self, validated_data):
        order_id = self.context.get('order_id')
        try:
            order_item_obj = models.OrderItem.objects.create(order_id=order_id,**validated_data)
            return order_item_obj
        except MergeExistingItemException as e:
            return {
                'message': e.message,
            }
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})