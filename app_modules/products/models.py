from django.db import models
from app_modules.base.models import BaseModel
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

users = get_user_model()

class Category(BaseModel):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

class Products(BaseModel):
    name     = models.CharField(max_length=512)
    stock    = models.PositiveIntegerField(default=0)
    price    = models.DecimalField(max_digits=10, decimal_places=2,default=0) 
    vendor   = models.ForeignKey(users, related_name="vendor_products", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category,related_name="category_product",on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.vendor and self.vendor.type != users.VENDOR:
            raise ValidationError("The selected user must be a vendor.")
        
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=['vendor', 'category','name', 'stock']),
        ]

class ProductImage(BaseModel):
    image   = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Products, related_name='product_images', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
    
class ProductReview(BaseModel):
    comment = models.TextField(blank=True)
    rating  = models.PositiveIntegerField() 
    product = models.ForeignKey(Products, related_name='product_reviews', on_delete=models.CASCADE)
    user    = models.ForeignKey(users, related_name='user_review', on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.id}"
    
class ReviewImage(BaseModel):
    image   = models.ImageField(upload_to='review/')
    review  = models.ForeignKey(ProductReview, related_name='review_images', on_delete=models.CASCADE)

    def __str__(self):
        return self.review.product.name
    
class StockHistory(BaseModel):

    IN    = "in"
    OUT   = "out"

    TYPE_CHOICES = (
        (IN,IN),
        (OUT,OUT),
    )
    
    change_amount = models.IntegerField()
    type          = models.CharField(choices=TYPE_CHOICES, max_length=20,default=IN)
    product       = models.ForeignKey(Products, related_name='product_stock_history', on_delete=models.CASCADE)
    user          = models.ForeignKey(users, related_name="stock_user", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product.name}-{self.type}"

    class Meta:
        verbose_name_plural = "Stock Histories"