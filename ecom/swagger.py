from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="E-com API",
        default_version='v1',
        description="API for E-com Project you can login with following credentials \n email='admin@gmail.com' \n pass='Admin@123' \n and in Authorize section add 'Bearer'+1 space+'access token'  to test all api",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# from rest_framework import serializers
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# class TokenObtainPairSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)

# # Use the decorator to modify the Swagger UI for TokenObtainPairView
# @swagger_auto_schema(request_body=TokenObtainPairSerializer)
# class CustomTokenObtainPairView(TokenObtainPairView):
#     pass