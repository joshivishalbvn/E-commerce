from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView 
from app_modules.users import serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from app_modules.base.viewset import BaseViewSet
from django.contrib.auth import login , authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterUserView(APIView):

    permission_classes = [AllowAny]
    serializer_class = serializers.UserRegistrationSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"User Registered Successfully..."},status=status.HTTP_201_CREATED)
    
class UserLoginView(APIView):
    from drf_yasg.utils import swagger_auto_schema

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=serializers.UserLoginSerializer)
    def post(self,request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user:
            login(request, user)

            refresh = RefreshToken.for_user(user)

            return Response({
                    'message': "Login Successful...",
                    'user': serializers.UserBasicDetailsSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    
class UserViewSet(BaseViewSet):

    serializer_class = serializers.UserBasicDetailsSerializer

    def get_queryset(self):
        qs        = User.objects.all()
        name      = self.request.query_params.get("name")
        user_type = self.request.query_params.get("type")

        filters = Q()
        if name:
            filters |= (
                Q(email__icontains=name) |
                Q(first_name__icontains=name) |
                Q(last_name__icontains=name)
            )

        if user_type:
            filters &= Q(type=user_type)

        return qs.filter(filters)
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception:
            return self.handle_not_found("User")
    
class UpdateVendorOrCustomerView(APIView):

    def put(self,request,pk):
        user_obj = get_object_or_404(User,id=pk)
        serializer = serializers.UserRegistrationSerializer(
            user_obj,
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Details Updated Successfully..."},status=status.HTTP_200_OK)