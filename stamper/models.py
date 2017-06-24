from django.db import models


class WebPage(models.Model):
    PENDING = 0
    WAITING=1
    CONFIRMED = 2
    STATUSES = (
        (PENDING, 'Pending'),
        (WAITING, 'Waiting'),
        (CONFIRMED, 'Confirmed'),
    )

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, null=True, blank=True, default="")
    url = models.URLField()
    address = models.CharField(max_length=20, null=True, blank=True, default="")
    status = models.IntegerField(default=0, choices=STATUSES)
    tx = models.CharField(max_length=64, null=True, blank=True, default="")

    class Meta:
        ordering = ('created',)
        get_latest_by = "created"

    def __str__(self):
        return self.url
