from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from app_modules.base.viewset import BaseViewSet
from rest_framework.generics import GenericAPIView
from app_modules.products import models , serializers

class ProductViewSet(BaseViewSet):

    serializer_classes = [serializers.ProductDataSerializer, serializers.ProductSerializer]
    model_class        = models.Products

    def get_dynamic_filters(self):
        
        filters = Q()
        
        name        = self.request.query_params.get("name")
        stock       = self.request.query_params.get("stock")
        vendor_id   = self.request.query_params.get("vendor_id")
        category_id = self.request.query_params.get("category_id")

        if vendor_id:
            filters &= Q(vendor_id=vendor_id)
        if category_id:
            filters &= Q(category_id=category_id)
        if name:
            filters &= Q(name__icontains=name)
        if stock is not None:
            filters &= Q(stock=stock)

        return filters

    def get_queryset(self):
        return self.model_class.objects.select_related("vendor", "category").prefetch_related("product_images", "product_reviews").filter(self.get_dynamic_filters())

    def get_serializer_class(self):
        return self.serializer_classes[0] if self.action in ['list', 'retrieve'] else self.serializer_classes[1]

    def create(self, request, *args, **kwargs):
        return super().create(request, entity_name="Product", *args, **kwargs)
       
    def update(self, request, *args, **kwargs):
        return super().update(request, entity_name="Product", *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception:
            return self.handle_not_found("Product")
        
class ProductImagesViewSet(BaseViewSet):

    serializer_class = serializers.ProductImagesSerializer

    def get_queryset(self):
        return models.ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))

    def get_serializer_context(self):
        ctx =  super().get_serializer_context()
        ctx["request"] = self.request
        ctx["product_id"] = self.kwargs.get('product_pk', None)
        return ctx
    
    def create(self, request, *args, **kwargs):
        return super().create(request, entity_name="Product Image", *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, entity_name="Product Image", *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception:
            return self.handle_not_found("Product Image")
        
class CategoryViewSet(BaseViewSet):

    serializer_class = serializers.CategorySerializer
    model_class      = models.Category
   
    def get_dynamic_filters(self):
        filters = Q()
        name = self.request.query_params.get("name")
        if name:
            filters &= Q(name__icontains=name)
        return filters
    
    def create(self, request, *args, **kwargs):
        return super().create(request, entity_name="Category", *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, entity_name="Category", *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception:
            return self.handle_not_found("Category")
        
class ProductReviewViewSet(BaseViewSet):

    serializer_classes = [serializers.ProductReviewDataSerializer,serializers.ProductReviewSerializer]
    model_class        = models.ProductReview

    def get_dynamic_filters(self):
        filters = Q()
        name = self.request.query_params.get("name")
        if name:
            filters &= Q(product__name__icontains=name)
        return filters
    
    def get_queryset(self):
        return self.model_class.objects.select_related("user").prefetch_related("review_images").filter(self.get_dynamic_filters())

    def get_serializer_class(self):
        return self.serializer_classes[0] if self.action in ['list', 'retrieve'] else self.serializer_classes[1]

    def create(self, request, *args, **kwargs):
        return super().create(request, entity_name="Product Review", *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, entity_name="Product Review", *args, **kwargs)
    
class ProductReviewImagesViewSet(BaseViewSet):

    serializer_class = serializers.ProductReviewImagesSerializer

    def get_queryset(self):
        return models.ReviewImage.objects.filter(review_id=self.kwargs.get('review_pk'))

    def get_serializer_context(self):
        ctx =  super().get_serializer_context()
        ctx["review_id"] = self.kwargs.get('review_pk')
        ctx["request"] = self.request
        return ctx
    
    def create(self, request, *args, **kwargs):
        return super().create(request, entity_name="Product Review Image", *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, entity_name="Product Review Image", *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception:
            return self.handle_not_found("Product Review Image")
        
class StockCreateView(APIView):

    def post(self,request,product_id):
        serializer = serializers.StockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_obj = get_object_or_404(models.Products,id=product_id)
        product_obj.stock += serializer.validated_data["stock"]
        product_obj.save()
        models.StockHistory.objects.create(
            change_amount = serializer.validated_data["stock"],
            type = models.StockHistory.IN,
            product_id = product_id,
            user = self.request.user
        )
        return Response({"message": "Stock Added Successfully..."})
    
class StockHistoryView(GenericAPIView):
    
    def get(self, request):
        filters = Q()
        type = request.query_params.get("type")
        product_id = request.query_params.get("product_id")

        if product_id:
            filters &= Q(product_id=product_id)
        if type:
            filters &= Q(type=type)

        qs = models.StockHistory.objects.filter(filters).select_related("product", "user")
        
        page = self.paginate_queryset(qs)
        serializer = serializers.StockHistorySerializer(page, many=True)

        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)