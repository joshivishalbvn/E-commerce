from django.urls import include, path

urlpatterns = [
    path('', include("app_modules.users.urls")),
    path('', include("app_modules.products.urls")),
    path('', include("app_modules.orders.urls")),
]
