from decimal import Decimal
from django.db import models
from app_modules.base.models import BaseModel
from django.contrib.auth import get_user_model
from app_modules.products.models import Products

User = get_user_model()

class Order(BaseModel):

    PENDING   = "pending"
    COMPLETED = "completed"
    CANCELED  = "canceled"

    STATUS_CHOICES = (
        (PENDING,PENDING),
        (COMPLETED,COMPLETED),
        (CANCELED,CANCELED),
    )

    customer     = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount     = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        indexes = [
            models.Index(fields=['customer', 'created_at']),
        ]

    def save(self, *args, **kwargs):
        self.total_amount = Decimal(self.total_amount) if isinstance(self.total_amount, float) else self.total_amount
        self.discount = Decimal(self.discount) if isinstance(self.discount, float) else self.discount
        self.final_amount = self.total_amount - self.discount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.customer.email} - Status: {self.status}"
    
class OrderItem(BaseModel):
    quantity = models.PositiveIntegerField()
    product  = models.ForeignKey(Products, on_delete=models.CASCADE)
    price    = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    order    = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    total    = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    class Meta:
        indexes = [
            models.Index(fields=['order', 'product']),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"

class Payment(BaseModel):

    PENDING   = "pending"
    COMPLETED = "completed"
    CANCELED  = "canceled"

    STATUS_CHOICES = (
        (PENDING,PENDING),
        (COMPLETED,COMPLETED),
        (CANCELED,CANCELED),
    )

    payment_method  = models.CharField(max_length=50) 
    payment_date    = models.DateTimeField(auto_now_add=True)
    amount          = models.DecimalField(max_digits=10, decimal_places=2)
    order           = models.OneToOneField(Order, on_delete=models.CASCADE)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Payment for Order {self.order.id} - Amount: {self.amount} - Status: {self.status}"