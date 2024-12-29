from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from app_modules.base.viewset import BaseViewSet
from app_modules.orders import models , serializers
from app_modules.base.services import StripeService

class OrderViewSet(BaseViewSet):

    model_class = models.Order
    serializer_classes = [serializers.OrderDataSerializer, serializers.OrderSerializer]

    def get_serializer_class(self):
        return self.serializer_classes[0] if self.action in ['list', 'retrieve'] else self.serializer_classes[1]
    
    def parse_date(self, date_str):
        try:
            return timezone.datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            return None
    
    def get_dynamic_filters(self):
        filters    = Q()
        customer   = self.request.query_params.get("customer")
        start_date = self.request.query_params.get("start_date")
        end_date   = self.request.query_params.get("end_date")

        if customer:
            customer_id = int(customer) if customer.isdigit() else None

            filters |= Q(customer__first_name__icontains=customer)
            filters |= Q(customer__last_name__icontains=customer)
            filters |= Q(customer__email=customer)
            filters |= Q(customer_id=customer_id)

        if start_date:
            filters &= (Q(created_at__gte=self.parse_date(start_date)))

        if end_date:
            filters &= (Q(created_at__lte=self.parse_date(end_date)))

        return filters
    
    def get_queryset(self):
        return self.model_class.objects.select_related("customer").prefetch_related("order_items__product").filter(self.get_dynamic_filters())
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, entity_name="Order", *args, **kwargs)
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
    
    def update(self, request, *args, **kwargs):
        return super().update(request, entity_name="Order", *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception:
            return self.handle_not_found("Order")
        
class OrderProductViewSet(BaseViewSet):

    serializer_class = serializers.OrderProductDataSerializer

    def get_queryset(self):
        return models.OrderItem.objects.select_related("product").filter(order_id=self.kwargs.get('order_pk'))
    
    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["order_id"] = self.kwargs.get('order_pk')
        ctx["request"] = self.request
        return ctx
    
    def create(self, request, *args, **kwargs):
        return super().create(request, entity_name="Order Product", *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, entity_name="Order Product", *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception:
            return self.handle_not_found("Order Product")
        
class CreatePaymentView(APIView):
    
    def post(self, request):
        payment_method_id = request.data.get('payment_method_id')
        
        try:
            order = models.Order.objects.get(id=request.data.get('order_id'))
            stripe_service = StripeService()
            
            payment_intent = stripe_service.create_payment_intent(order.final_amount, payment_method_id)

            if payment_intent['status'] != 'succeeded':
                return Response({'error': 'Payment not successful'}, status=status.HTTP_400_BAD_REQUEST)

            models.Payment.objects.create(
                order=order,
                amount=order.final_amount,
                payment_method=payment_method_id,
                status=models.Payment.COMPLETED,
            )

            order.status = models.Order.COMPLETED
            order.save()

            return Response({'payment_intent': payment_intent}, status=status.HTTP_200_OK)
            
        except models.Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)