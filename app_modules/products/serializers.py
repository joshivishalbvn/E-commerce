from rest_framework import serializers
from app_modules.products import models
from rest_framework.exceptions import ValidationError
from app_modules.users.serializers import UserBasicDetailsSerializer
from .tasks import process_product_images, process_product_review_images

class ProductDataSerializer(serializers.ModelSerializer):

    category = serializers.SerializerMethodField()
    vendor   = serializers.SerializerMethodField()
    images   = serializers.SerializerMethodField()
    reviews  = serializers.SerializerMethodField()

    class Meta:
        model  = models.Products
        fields = (
            "id",
            "name",
            "price",
            "category",
            "vendor",
            "stock",
            "images",
            "reviews",
        )
    
    def get_vendor(self,obj):
        return UserBasicDetailsSerializer(obj.vendor).data if obj.vendor else "---"
    
    def get_category(self,obj):
        return CategorySerializer(obj.category).data if obj.category else "---"
    
    def get_images(self,obj):
        return ProductImagesSerializer(
            obj.product_images.all(),
            many=True,
            context={"request" : self.context.get('request')}
        ).data
    
    def get_reviews(self,obj):
        return ProductReviewDataSerializer(
            obj.product_reviews.all(),
            many=True,
            context={"request" : self.context.get('request')}
        ).data

class ProductBasicDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model  = models.Products
        fields = (
            "id",
            "name",
        )

class ProductSerializer(serializers.ModelSerializer):

    images = serializers.ListField(required=False)

    class Meta:
        model  = models.Products
        fields = (
            "name",
            "category",
            "price",
            "vendor",
            "images"
        )

    def create(self, validated_data):
        images_data = validated_data.pop("images",[])
        product_obj = models.Products(**validated_data)
        product_obj.save()
        if images_data:
            process_product_images(product_obj.id, images_data)
        return product_obj
    
class ProductImagesSerializer(serializers.ModelSerializer):

    id  = serializers.ReadOnlyField()

    class Meta:
        model  = models.ProductImage
        fields = (
            "id",
            "image",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self.get_full_url(instance)
        return representation
    
    def get_full_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if request and obj.image else None
    
    def create(self, validated_data):
        product_image_obj = models.ProductImage.objects.create(
            product_id=self.context.get('product_id'),
            **validated_data
        )
        return product_image_obj
    
class CategorySerializer(serializers.ModelSerializer):

    id  = serializers.ReadOnlyField()

    class Meta:
        model  = models.Category
        fields =(
            "id",
            "name"
        )

class ProductReviewDataSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()
    user   = serializers.SerializerMethodField()

    class Meta:
        model  = models.ProductReview
        fields =(
            "id",
            "product",
            "user",
            "rating",
            "comment",
            "images",
        )

    def get_images(self,obj):
        return ProductReviewImagesSerializer(
            obj.review_images.all()
            ,many=True,
            context={"request":self.context.get('request')}
        ).data
    
    def get_user(self,obj):
        return UserBasicDetailsSerializer(obj.user).data if obj.user else None
    
class ProductReviewSerializer(serializers.ModelSerializer):

    images = serializers.ListField(required=False)

    class Meta:
        model  = models.ProductReview
        fields =(
            "product",
            "rating",
            "comment",
            "images",
        ) 

    def create(self, validated_data):
        review_images = validated_data.pop("images",[])
        review_obj = models.ProductReview.objects.create(
            user=self.context.get('user'),
            **validated_data
        )
        process_product_review_images(review_obj.id,review_images)
        return review_obj

class ProductReviewImagesSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model  = models.ReviewImage
        fields = (
            "id",
            "image",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self.get_full_url(instance)
        return representation
    
    def get_full_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if request and obj.image else None
    
    def create(self, validated_data):
        review_image_obj = models.ReviewImage.objects.create(
            review_id=self.context.get('review_id'),
            **validated_data
        )
        return review_image_obj
    
class StockSerializer(serializers.Serializer):

    stock = serializers.IntegerField()

    def validate_stock(self, value):
        value = value
        if value > 0:
            return value
        raise ValidationError("Stock Should Be More Than 0")
    
class StockHistorySerializer(serializers.ModelSerializer):

    product    = serializers.SerializerMethodField()
    user       = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model  = models.StockHistory
        fields = (
            "id",
            "product",
            "change_amount",
            "type",
            "user",
            "created_at",
        )

    def get_product(self,obj):
        return ProductBasicDetailsSerializer(obj.product).data
    
    def get_user(self,obj):
        return UserBasicDetailsSerializer(obj.user).data