from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

# استيراد الموديلز من تطبيق المحتوى وتطبيق الإحصائيات
from content.models import News, Event, Service, Facility
from .models import MonthlyStat, SectorStat

# دالة مساعدة لتحديث أو إنشاء الإحصائيات الشهرية والقطاعية
def modify_stats(instance, action, field_name):
    """
    action: 'add' لزيادة العداد، أو 'delete' لإنقاص العداد
    field_name: اسم الحقل المراد تحديثه مثل ('news', 'events', 'services', 'facilities')
    """
    amount = 1 if action == 'add' else -1
    
    # --- 1. تحديث الإحصائيات الشهرية (MonthlyStat) ---
    current_date = timezone.now()
    month_en = current_date.strftime("%B")  # اسم الشهر بالإنجليزية مثل "June"
    month_ar = current_date.strftime("%m")  # يمكنك تخصيص الاسم العربي لاحقاً، حالياً سنضع رقم الشهر أو اسمه
    
    monthly_stat, _ = MonthlyStat.objects.get_or_create(
        month_en=month_en,
        defaults={'month': month_ar}
    )
    # زيادة أو نقصان العداد الفعلي بالشهر
    current_month_val = getattr(monthly_stat, field_name)
    setattr(monthly_stat, field_name, max(0, current_month_val + amount))
    monthly_stat.save()

    # --- 2. تحديث إحصائيات القطاع (SectorStat) ---
    if hasattr(instance, 'sector') and instance.sector:
        sector_stat, _ = SectorStat.objects.get_or_create(sector=instance.sector)
        
        current_sector_val = getattr(sector_stat, field_name)
        setattr(sector_stat, field_name, max(0, current_sector_val + amount))
        sector_stat.save()


# ==================== الإشارات (Signals) ====================

# أولاً: الأخبار (News)
@receiver(post_save, sender=News)
def news_saved(sender, instance, created, **kwargs):
    if created:
        modify_stats(instance, 'add', 'news')

@receiver(post_delete, sender=News)
def news_deleted(sender, instance, **kwargs):
    modify_stats(instance, 'delete', 'news')


# ثانياً: الفعاليات (Event)
@receiver(post_save, sender=Event)
def event_saved(sender, instance, created, **kwargs):
    if created:
        modify_stats(instance, 'add', 'events')

@receiver(post_delete, sender=Event)
def event_deleted(sender, instance, **kwargs):
    modify_stats(instance, 'delete', 'events')


# ثالثاً: الخدمات (Service)
@receiver(post_save, sender=Service)
def service_saved(sender, instance, created, **kwargs):
    if created:
        modify_stats(instance, 'add', 'services')

@receiver(post_delete, sender=Service)
def service_deleted(sender, instance, **kwargs):
    modify_stats(instance, 'delete', 'services')


# رابعاً: المنشآت (Facility)
@receiver(post_save, sender=Facility)
def facility_saved(sender, instance, created, **kwargs):
    if created:
        modify_stats(instance, 'add', 'facilities')

@receiver(post_delete, sender=Facility)
def facility_deleted(sender, instance, **kwargs):
    modify_stats(instance, 'delete', 'facilities')