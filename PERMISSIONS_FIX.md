# 🔐 توثيق حل مشكلة Permissions

## المشكلة الأساسية 🚨
Admin قطاع الرياضة كان يستطيع الوصول والتعديل والحذف لبيانات قطاعات أخرى (التعليم والصحة)

## الحل 🎯

### 1️⃣ تحديث Permissions Class في `accounts/premissions.py`

**التغييرات:**
- أضفنا فحص `hasattr(obj, 'sector')` للتأكد من أن الـ object لديه حقل sector
- السوبر أدمن يحصل على وصول كامل لكل شيء
- الـ Admin يستطيع فقط العمل مع بيانات قطاعه (مقارنة `obj.sector == request.user.sector`)

```python
def has_object_permission(self, request, view, obj):
    # superadmin يعمل أي شيء
    if request.user.role == "superadmin":
        return True

    # admin فقط ضمن نفس القطاع
    if not hasattr(obj, 'sector'):
        return False
    
    return obj.sector == request.user.sector
```

---

### 2️⃣ إنشاء `SectorFilteredViewSet` في `content/views.py`

**الفكرة:**
- ViewSet قاعدة يقوم بـ filtering تلقائي للبيانات

**ما يفعله:**
```python
class SectorFilteredViewSet(ModelViewSet):
    permission_classes = [IsSectorAdminOrSuperAdmin]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # superadmin يرى كل البيانات
        if user.role == "superadmin":
            return queryset
        
        # admin يرى فقط بيانات قطاعه
        if user.role == "admin" and user.sector:
            return queryset.filter(sector=user.sector)
        
        return queryset.none()
```

**النتيجة:**
- كل الـ ViewSets (News, History, Services, Facilities, Events) ترث من هذه القاعدة
- تطبيق Permissions + Filtering تلقائي

---

### 3️⃣ تحديث `comments/views.py`

**أضفنا Filtering للـ Inquiries:**
```python
def get_queryset(self):
    user = self.request.user
    queryset = Inquiry.objects.all().order_by("-id")
    
    # superadmin يرى كل الاستفسارات
    if user.role == "superadmin":
        return queryset
    
    # admin يرى فقط استفسارات قطاعه
    if user.role == "admin" and user.sector:
        return queryset.filter(sector=user.sector)
    
    return queryset.none()
```

---

## 🔒 آلية الحماية على مستويين

### **المستوى الأول: List/Retrieve (عرض البيانات)**
```
GET /api/content/events/  ← يرى فقط بيانات قطاعه
```
- الـ `get_queryset()` يفلتر البيانات تلقائياً
- Admin الرياضة لن يرى أحداث التعليم أصلاً

### **المستوى الثاني: Create/Update/Delete (تعديل البيانات)**
```
POST/PATCH/DELETE /api/content/events/{id}/  
```
- الـ `IsSectorAdminOrSuperAdmin` Permission يتحقق من `has_object_permission`
- يتأكد من أن البيانات المراد تعديلها/حذفها من قطاع المستخدم

---

## 📋 السيناريوهات المختلفة

### ✅ Superadmin
| العملية | النتيجة |
|--------|--------|
| عرض كل الأحداث | ✅ يرى الكل |
| إضافة حدث | ✅ يستطيع في أي قطاع |
| تعديل أي حدث | ✅ يستطيع تعديل أي حدث |
| حذف أي حدث | ✅ يستطيع حذف أي حدث |

### ✅ Admin (الرياضة)
| العملية | النتيجة |
|--------|--------|
| عرض الأحداث | ✅ يرى فقط أحداث الرياضة |
| إضافة حدث | ✅ يضيف في الرياضة فقط |
| تعديل حدث الرياضة | ✅ يستطيع |
| تعديل حدث التعليم | ❌ `403 Forbidden` |
| حذف حدث الرياضة | ✅ يستطيع |
| حذف حدث التعليم | ❌ `403 Forbidden` |

---

## 🧪 كيفية الاختبار

### **اختبار سريع بـ Python Shell**
```bash
python manage.py shell
```

```python
from accounts.models import User
from content.models import Event

# إنشاء مستخدمين
admin_sports = User.objects.create_user(
    username='admin_sports',
    password='pass',
    role='admin',
    sector='sports'
)

admin_edu = User.objects.create_user(
    username='admin_edu',
    password='pass',
    role='admin',
    sector='education'
)

# إنشاء أحداث
event_sports = Event.objects.create(
    title_ar='حدث رياضي',
    title_en='Sports',
    sector='sports',
    date='2026-06-01'
)

event_edu = Event.objects.create(
    title_ar='حدث تعليمي',
    title_en='Education',
    sector='education',
    date='2026-06-01'
)

# اختبار الحذف
# admin_sports يحاول حذف حدث التعليم
from rest_framework.test import APIRequestFactory
from content.views import EventViewSet

factory = APIRequestFactory()
view = EventViewSet.as_view({'delete': 'destroy'})

# محاكاة طلب من admin_sports لحذف حدث التعليم
request = factory.delete(f'/events/{event_edu.id}/')
request.user = admin_sports
response = view(request, pk=event_edu.id)

print(f"Status Code: {response.status_code}")  # يجب أن يكون 403
```

### **اختبار بـ API/Postman**
```bash
# 1. تسجيل الدخول
POST http://localhost:8000/api/accounts/login/
{
    "username": "admin_sports",
    "password": "password"
}

# 2. محاولة عرض أحداث التعليم
GET http://localhost:8000/api/content/events/?sector=education
Headers: Authorization: Bearer {token}

# يجب أن ترى list فارغة (لا أحداث) لأن Admin الرياضة 
# لا يستطيع رؤية بيانات التعليم

# 3. محاولة حذف حدث من التعليم
DELETE http://localhost:8000/api/content/events/2/
Headers: Authorization: Bearer {token}

# يجب أن تحصل على 403 Forbidden
```

---

## 📁 الملفات المعدلة

| الملف | التغييرات |
|------|----------|
| `accounts/premissions.py` | ✅ تحديث `IsSectorAdminOrSuperAdmin.has_object_permission()` |
| `content/views.py` | ✅ إضافة `SectorFilteredViewSet` + تطبيقه على جميع ViewSets |
| `comments/views.py` | ✅ تحديث `InquiryViewSet.get_queryset()` للـ filtering |

---

## 🎯 الخلاصة

**الآن النظام:**
1. ✅ يمنع Admin الرياضة من رؤية بيانات قطاعات أخرى
2. ✅ يمنع Admin الرياضة من تعديل بيانات قطاعات أخرى
3. ✅ يمنع Admin الرياضة من حذف بيانات قطاعات أخرى
4. ✅ يسمح Superadmin بالوصول الكامل لكل شيء
5. ✅ Filtering تلقائي على مستوى Database Query (أفضل أداء)
6. ✅ Permission checks على مستوى Object (أمان إضافي)
