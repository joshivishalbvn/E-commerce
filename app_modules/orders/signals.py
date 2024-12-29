from .models import OrderItem
from django.dispatch import receiver
from django.db.models.signals import pre_save

class MergeExistingItemException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

@receiver(pre_save, sender=OrderItem)
def merge_order_item(sender, instance, **kwargs):
    existing_item = OrderItem.objects.filter(order=instance.order, product=instance.product).first()
    
    if existing_item and existing_item.price == instance.price:
        created_at = existing_item.created_at
        existing_item.quantity += instance.quantity
        existing_item.created_at = created_at
        
        pre_save.disconnect(merge_order_item, sender=OrderItem)
        existing_item.save()
        pre_save.connect(merge_order_item, sender=OrderItem)
        
        raise MergeExistingItemException("Order product merged successfully.")
