from django.db import models


class WebPage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    url = models.URLField()
    body = models.TextField()
    signature = models.CharField(max_length=64)

    class Meta:
        ordering = ('created',)
