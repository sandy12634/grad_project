from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView

urlpatterns = [
    # مسار تسجيل الدخول (يرجع التوكن وبيانات المستخدم)
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # مسار تجديد التوكن
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]