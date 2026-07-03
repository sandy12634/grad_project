from django.db import models

class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('answered', 'Answered'),
    ]

    name = models.CharField(max_length=100, blank=True, null=True)  # الاسم (اختياري)
    sector = models.CharField(max_length=100) # أو استخدام ChoiceField
    question = models.TextField()
    
    # جعل الجواب اختيارياً عند الإنشاء وقابل للتعديل لاحقاً
    answer = models.TextField(blank=True, null=True) 
    
    # جعل الحالة الافتراضية هي "قيد الانتظار"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"Inquiry by {self.name}"