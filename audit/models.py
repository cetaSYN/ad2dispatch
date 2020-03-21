from django.db import models

class AuditAction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
