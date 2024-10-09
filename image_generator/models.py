from django.db import models

# Create your models here.
from django.db import models

class GeneratedImage(models.Model):
    prompt = models.TextField()
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)