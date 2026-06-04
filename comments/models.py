from django.db import models

class Inquiry(models.Model):
    # تحديد قائمة الخيارات للقطاعات
    SECTOR_CHOICES = [
        ("sports", "Sports"),
        ("health", "Health"),
        ("education", "Education"),
    ]

    # تحديد قائمة الخيارات للحالة (كما هو متوقع في الفرونت آند)
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("answered", "Answered"),
    ]

    name = models.CharField(max_length=100, blank=True, null=True)  # الاسم (اختياري)
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES) # القطاع
    question = models.TextField()  # نص السؤال
    
    # الحقول الجديدة ليتوافق المودل مع واجهة الفرونت آند:
    answer = models.TextField(blank=True, null=True)  # الإجابة (تكون فارغة في البداية)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="pending"
    )  # حالة السؤال وتبدأ تلقائياً بـ "pending"
    
    # حقل التاريخ (تمت تسميته date ليطابق TypeScript)
    created_at = models.DateTimeField()  
 # إضافة ميزة ذكية للـ save لتغيير الحالة تلقائياً عند إضافة جواب
    def save(self, *args, **kwargs):
        if self.answer and self.answer.strip():  # إذا تم كتابة جواب وليس فارغاً
            self.status = "answered"            # تتغير الحالة فوراً إلى مجاب عليه
        else:
            self.status = "pending"             # إذا حُذف الجواب تعود الحالة إلى قيد الانتظار
        super().save(*args, **kwargs)

    def str(self):
        return f"{self.name or 'Anonymous'} - ({self.get_sector_display()}) - {self.status}"