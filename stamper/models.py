from django.db import models


class WebPage(models.Model):
    PENDING = 0
    CONFIRMED = 1
    STATUSES = (
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
    )

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    url = models.URLField()
    body = models.TextField()
    signature = models.BinaryField()
    status = models.IntegerField(default=0, choices=STATUSES)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.url
