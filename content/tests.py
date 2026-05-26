from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from content.models import Event, News


class SectorPermissionTests(TestCase):
    """اختبار permissions للتحقق من أن الـ admin يرى فقط بيانات قطاعه"""
    
    def setUp(self):
        """إنشاء بيانات اختبار"""
        self.client = APIClient()
        
        # إنشاء Superadmin
        self.superadmin = User.objects.create_user(
            username='superadmin_user',
            password='test_password',
            role='superadmin'
        )
        
        # إنشاء Admin للرياضة
        self.admin_sports = User.objects.create_user(
            username='admin_sports',
            password='test_password',
            role='admin',
            sector='sports'
        )
        
        # إنشاء Admin للتعليم
        self.admin_education = User.objects.create_user(
            username='admin_education',
            password='test_password',
            role='admin',
            sector='education'
        )
        
        # إنشاء Admin للصحة
        self.admin_health = User.objects.create_user(
            username='admin_health',
            password='test_password',
            role='admin',
            sector='health'
        )
        
        # إنشاء أحداث في قطاعات مختلفة
        self.event_sports = Event.objects.create(
            title_ar='حدث رياضي',
            title_en='Sports Event',
            description_ar='وصف الحدث',
            description_en='Event description',
            sector='sports',
            date='2026-06-01'
        )
        
        self.event_education = Event.objects.create(
            title_ar='حدث تعليمي',
            title_en='Education Event',
            description_ar='وصف الحدث',
            description_en='Event description',
            sector='education',
            date='2026-06-01'
        )
        
        self.event_health = Event.objects.create(
            title_ar='حدث صحي',
            title_en='Health Event',
            description_ar='وصف الحدث',
            description_en='Event description',
            sector='health',
            date='2026-06-01'
        )
    
    # ============ اختبارات List (عرض البيانات) ============
    
    def test_superadmin_sees_all_events(self):
        """Superadmin يجب أن يرى جميع الأحداث"""
        self.client.force_authenticate(user=self.superadmin)
        response = self.client.get('/api/content/events/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # جميع الأحداث الثلاثة
    
    def test_admin_sports_sees_only_sports_events(self):
        """Admin الرياضة يجب أن يرى فقط أحداث الرياضة"""
        self.client.force_authenticate(user=self.admin_sports)
        response = self.client.get('/api/content/events/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # حدث واحد فقط
        self.assertEqual(response.data[0]['sector'], 'sports')
    
    def test_admin_education_sees_only_education_events(self):
        """Admin التعليم يجب أن يرى فقط أحداث التعليم"""
        self.client.force_authenticate(user=self.admin_education)
        response = self.client.get('/api/content/events/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # حدث واحد فقط
        self.assertEqual(response.data[0]['sector'], 'education')
    
    # ============ اختبارات Retrieve (تفاصيل حدث واحد) ============
    
    def test_admin_sports_can_retrieve_own_event(self):
        """Admin الرياضة يجب أن يستطيع الحصول على تفاصيل حدث رياضي"""
        self.client.force_authenticate(user=self.admin_sports)
        response = self.client.get(f'/api/content/events/{self.event_sports.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_admin_sports_cannot_retrieve_other_sector_event(self):
        """Admin الرياضة يجب أن لا يستطيع الحصول على أحداث قطاعات أخرى"""
        self.client.force_authenticate(user=self.admin_sports)
        response = self.client.get(f'/api/content/events/{self.event_education.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ============ اختبارات Create (إضافة بيانات) ============
    
    def test_admin_sports_can_create_sports_event(self):
        """Admin الرياضة يجب أن يستطيع إضافة حدث رياضي"""
        self.client.force_authenticate(user=self.admin_sports)
        data = {
            'title_ar': 'حدث رياضي جديد',
            'title_en': 'New Sports Event',
            'description_ar': 'وصف',
            'description_en': 'description',
            'sector': 'sports',
            'date': '2026-07-01'
        }
        response = self.client.post('/api/content/events/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.filter(sector='sports').count(), 2)
    
    def test_admin_sports_cannot_create_other_sector_event(self):
        """Admin الرياضة لا يستطيع إضافة حدث لقطاع آخر (إن تم المحاولة)"""
        self.client.force_authenticate(user=self.admin_sports)
        data = {
            'title_ar': 'حدث تعليمي',
            'title_en': 'Education Event',
            'description_ar': 'وصف',
            'description_en': 'description',
            'sector': 'education',  # محاولة إضافة في قطاع آخر
            'date': '2026-07-01'
        }
        response = self.client.post('/api/content/events/', data)
        
        # يجب أن يرفضه (403) أو يتجاهل وينشئ بقطاع المستخدم
        # حسب التطبيق - يمكن تعديل السيريالايزر لمنع هذا
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])
    
    # ============ اختبارات Update (تعديل البيانات) ============
    
    def test_admin_sports_can_update_own_event(self):
        """Admin الرياضة يجب أن يستطيع تعديل حدثه الخاص"""
        self.client.force_authenticate(user=self.admin_sports)
        data = {'title_ar': 'حدث رياضي محدّث'}
        response = self.client.patch(f'/api/content/events/{self.event_sports.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event_sports.refresh_from_db()
        self.assertEqual(self.event_sports.title_ar, 'حدث رياضي محدّث')
    
    def test_admin_sports_cannot_update_other_sector_event(self):
        """Admin الرياضة لا يستطيع تعديل أحداث قطاعات أخرى"""
        self.client.force_authenticate(user=self.admin_sports)
        data = {'title_ar': 'تعديل غير مصرح'}
        response = self.client.patch(f'/api/content/events/{self.event_education.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ============ اختبارات Delete (حذف البيانات) ============
    
    def test_admin_sports_can_delete_own_event(self):
        """Admin الرياضة يجب أن يستطيع حذف حدثه الخاص"""
        self.client.force_authenticate(user=self.admin_sports)
        response = self.client.delete(f'/api/content/events/{self.event_sports.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=self.event_sports.id).exists())
    
    def test_admin_sports_cannot_delete_other_sector_event(self):
        """Admin الرياضة لا يستطيع حذف أحداث قطاعات أخرى"""
        self.client.force_authenticate(user=self.admin_sports)
        response = self.client.delete(f'/api/content/events/{self.event_education.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Event.objects.filter(id=self.event_education.id).exists())
    
    def test_superadmin_can_delete_any_event(self):
        """Superadmin يجب أن يستطيع حذف أي حدث"""
        self.client.force_authenticate(user=self.superadmin)
        response = self.client.delete(f'/api/content/events/{self.event_education.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=self.event_education.id).exists())
    
    # ============ اختبارات مشاهدة (لا يجب أن يرى بيانات ليست له) ============
    
    def test_admin_sports_cannot_list_education_events(self):
        """عندما يطلب Admin الرياضة قائمة الأحداث، لا يجب أن يرى تعليم"""
        self.client.force_authenticate(user=self.admin_sports)
        response = self.client.get('/api/content/events/')
        
        sectors = [item['sector'] for item in response.data]
        self.assertNotIn('education', sectors)
        self.assertNotIn('health', sectors)
        self.assertIn('sports', sectors)
