# from celery import shared_task
from app_modules.products import models

# @shared_task()
def process_product_images(product_id, images_data):
    product_obj = models.Products.objects.get(id=product_id)
    product_images = [
        models.ProductImage(product=product_obj, image=image) for image in images_data
    ]
    models.ProductImage.objects.bulk_create(product_images)
    print(">>>>>>>>>>>> PRODUCT IMAGES UPLOADED <<<<<<<<<<<<")

def process_product_review_images(review_id, images_data):
    review_obj = models.ProductReview.objects.get(id=review_id)
    review_images = [
        models.ReviewImage(review=review_obj, image=image) for image in images_data
    ]
    models.ReviewImage.objects.bulk_create(review_images)
    print(">>>>>>>>>>>> PRODUCT REVIEW IMAGES UPLOADED <<<<<<<<<<<<")