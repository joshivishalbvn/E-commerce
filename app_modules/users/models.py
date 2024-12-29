from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
    
    ADMIN    = "Admin"
    VENDOR   = "Vendor"
    CUSTOMER = "Customer"

    TYPE_CHOICES = (
        (ADMIN,ADMIN),
        (VENDOR,VENDOR),
        (CUSTOMER,CUSTOMER),
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD  = "email"
    email           = models.EmailField(unique=True)
    username        = models.CharField(blank=True,null=True)
    type            = models.CharField(choices=TYPE_CHOICES, max_length=20,default=ADMIN)

    def __str__(self):
        return self.get_full_name()

# class CustomerManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return super().get_queryset(*args, **kwargs).filter(role=Users.CUSTOMER)
    
# class Customers(Users):
#     role = Users.CUSTOMER
#     objects = CustomerManager()
    
#     class Meta:
#         proxy = True

# class VendorManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return super().get_queryset(*args, **kwargs).filter(role=Users.VENDOR)
    
# class Vendors(Users):
#     role = Users.VENDOR
#     objects = VendorManager()
    
#     class Meta:
#         proxy = True