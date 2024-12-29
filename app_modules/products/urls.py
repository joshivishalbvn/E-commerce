from django.urls import path
from app_modules.products import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"products",views.ProductViewSet,basename="product")
router.register(r"categories",views.CategoryViewSet,basename="category")
router.register(r'products/(?P<product_pk>\d+)/images', views.ProductImagesViewSet, basename='product-images')
router.register(r'products/(?P<product_pk>\d+)/review', views.ProductReviewViewSet, basename='product-review')
router.register(r'review/(?P<review_pk>\d+)/images', views.ProductReviewImagesViewSet, basename='review-images')

urlpatterns = [
    path("product/stock-history",views.StockHistoryView.as_view(),name="create_stock"),
    path("product/<int:product_id>/stock",views.StockCreateView.as_view(),name="create_stock"),
]

urlpatterns += router.urls