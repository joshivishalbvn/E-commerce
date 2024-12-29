from .models import *
from django.contrib import admin

# Register your models here.

class StockHistoryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False  

admin.site.register(Products)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(ProductReview)
admin.site.register(ReviewImage)
admin.site.register(StockHistory, StockHistoryAdmin)