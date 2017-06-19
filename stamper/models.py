from django.db import models


class WebPage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    url = models.URLField()
    body = models.TextField()
    signature = models.BinaryField()

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.url
