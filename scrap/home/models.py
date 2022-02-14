from django.db import models

class Clone(models.Model):
    url = models.TextField()
    created = models.DateTimeField(auto_now_add=True)