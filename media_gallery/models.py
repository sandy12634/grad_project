import os
from django.db import models
from django.core.exceptions import ValidationError

def validate_media_file(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.svg', '.mp4', '.mov', '.avi', '.webm']
    if not ext in valid_extensions:
        raise ValidationError('يمكنك رفع صور أو فيديوهات فقط!')

class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'image'),
        ('video', 'video'),
    ]

    # حقول الوصف (تطابق description_ar و description_en بالصورة)
    description_ar = models.TextField(max_length=800,null=True , blank=True)
    description_en = models.TextField(max_length=800,null=True , blank=True)
    
    # حقل تحديد النوع (يطابق type: "image" | "video")
    type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    
    # حقل الملف (والذي سيتحول إلى url كامل عند إرساله للفرونت إند)
    url = models.FileField(upload_to='media_gallery/', validators=[validate_media_file] , null=True , blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Media Gallery"

    def str(self):
        return f"{self.type} - {self.description_en[:30] if self.description_en else self.id}"

    # دالة لتحديد النوع تلقائياً بناءً على امتداد الملف عند الحفظ بالـ Admin
    def save(self, *args, **kwargs):
        if self.url:
            ext = os.path.splitext(self.url.name)[1].lower()
            if ext in ['.mp4', '.mov', '.avi', '.webm']:
                self.type = 'video'
            else:
                self.type = 'image'
        super().save(*args, **kwargs)
