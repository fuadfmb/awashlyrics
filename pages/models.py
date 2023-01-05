from django.db import models

class Page(models.Model):
    page_created_at = models.DateTimeField()
    page_slug  = models.CharField(max_length=100, unique=True)
    page_title = models.CharField(max_length=100)
    page_body  = models.TextField()
    
    def __str__(self):
        return self.page_slug
    class Meta:
        ordering = ['page_slug']
