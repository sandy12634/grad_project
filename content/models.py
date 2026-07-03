
from django.db import models

class BaseContent(models.Model):
    SECTOR_CHOICES = [
        ('sports', 'sports'),
        ('health', 'health'),
        ('education', 'education'),
    ]

    title_ar = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_ar = models.TextField()
    description_en = models.TextField()
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class News(BaseContent):
    date = models.DateField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)


class History(BaseContent):
    image = models.ImageField(upload_to='history/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Histories"


class Service(BaseContent):
    cost = models.CharField(max_length=100, null=True, blank=True)


class Facility(BaseContent):
    image = models.ImageField(upload_to='facilities/', null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address_ar = models.CharField(max_length=255)
    address_en = models.CharField(max_length=255)


class Event(BaseContent):
    date = models.DateField()
    image = models.ImageField(upload_to='events/',null=True, blank=True)