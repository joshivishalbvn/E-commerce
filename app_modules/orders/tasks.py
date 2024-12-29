from django.db import transaction
from app_modules.orders import models
from django.contrib.auth import get_user_model
from app_modules.products.models import StockHistory

user = get_user_model()

# @shared_task()
def process_order_items(order_id, product_data):
    try:
        with transaction.atomic():
            print('\033[91m' + 'product_data: ' + '\033[92m', product_data)

            # Prepare to create OrderItems
            order_products = []
            for product in product_data:
                product_obj = models.Products.objects.filter(id=product["id"]).first()
                print('\033[91m' + 'product_obj: ' + '\033[92m', product_obj)

                if product_obj:  # Check if product exists
                    order_item = models.OrderItem(
                        order_id=order_id,
                        product_id=product["id"],
                        quantity=product["quantity"],
                        price=product_obj.price,
                        total=product_obj.price * product["quantity"]
                    )
                    order_products.append(order_item)

            # Bulk create OrderItems once
            if order_products:
                models.OrderItem.objects.bulk_create(order_products)
                print(">>>>>>>>>>>> ORDER PRODUCT CREATED <<<<<<<<<<<<")

            # Find the superuser for stock updates
            super_user = user.objects.filter(is_superuser=True).first()
            if not super_user:
                raise Exception("No superuser found.")
            
            # Prepare stock history entries
            product_history = [
                StockHistory(product_id=product["id"], change_amount=product["quantity"], type=StockHistory.OUT, user=super_user) 
                for product in product_data
            ]
            StockHistory.objects.bulk_create(product_history)

            # Prepare product updates in bulk
            updated_products = []
            for product in product_data:
                product_obj = models.Products.objects.get(id=product["id"])
                product_obj.stock -= product["quantity"]
                updated_products.append(product_obj)

            # Bulk update product stocks
            if updated_products:
                models.Products.objects.bulk_update(updated_products, ["stock"])
                print(">>>>>>>>>>>> PRODUCT HISTORY UPDATED <<<<<<<<<<<<")

    except Exception as e:
        print(f"Error occurred: {e}")
