from django.urls import path
from app_modules.orders import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"orders",views.OrderViewSet,basename="order")
router.register(r'orders/(?P<order_pk>\d+)/products', views.OrderProductViewSet, basename='order-product')

urlpatterns = [
    path('create-payment/', views.CreatePaymentView.as_view(), name='create_payment'),
]

urlpatterns += router.urls