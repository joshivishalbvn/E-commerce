from django.db import models

class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']  