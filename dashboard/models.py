from django.db import models

# إذا أردتِ استخدام خيارات القطاعات، يمكنكِ استيرادها من تطبيق accounts 
# لمنع التكرار، أو كتابتها هنا مجدداً.
SECTOR_CHOICES = [
    ("sports", "sports"),
    ("health", "health"),
    ("education", "education"),
]

class MonthlyStat(models.Model):
    month = models.CharField(max_length=50)
    month_en = models.CharField(max_length=50)
    news = models.IntegerField(default=0)
    events = models.IntegerField(default=0)
    services = models.IntegerField(default=0)
    facilities = models.IntegerField(default=0)

    def __str__(self):
        return f"Monthly Stats - {self.month_en}"

class SectorStat(models.Model):
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES, unique=True)
    news = models.IntegerField(default=0)
    events = models.IntegerField(default=0)
    services = models.IntegerField(default=0)
    facilities = models.IntegerField(default=0)

    def __str__(self):
        return f"Sector Stats - {self.sector}"