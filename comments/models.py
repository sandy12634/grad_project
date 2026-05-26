from django.db import models

class Inquiry(models.Model):
    
    
    # 1. تحديد قائمة الخيارات (الاختبار)
   SECTOR_CHOICES = [
    ("sports", "sports"),
    ("health", "health"),
    ("education", "education"),
    ]

    
   name = models.CharField(max_length=100, blank=True, null=True) # الاسم اختياري
 
   sector = models.CharField(
        max_length=50, 
        choices=SECTOR_CHOICES, 
               
    )    
   question = models.TextField() # نص السؤال
   created_at = models.DateTimeField(auto_now_add=True) # وقت إرسال السؤال

def __str__(self):
        return f"{self.name or 'Anonymous'} - {self.sector}"