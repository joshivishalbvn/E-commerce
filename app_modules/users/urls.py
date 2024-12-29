from django.urls import path
from app_modules.users import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users",views.UserViewSet,basename="user")

urlpatterns = [
    path("login/",views.UserLoginView.as_view(),name="user_login"),
    path("register/",views.RegisterUserView.as_view(),name="user_register"),
    path("user/<int:pk>/update/",views.UpdateVendorOrCustomerView.as_view(),name="update_user"),
]

urlpatterns += router.urls