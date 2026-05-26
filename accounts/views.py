from rest_framework import viewsets
from .premissions import IsSuperAdmin, IsAdminOrSuperAdmin, IsSectorAdminOrSuperAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
    
class InquiryViewSet(viewsets.ModelViewSet):
    # ... queryset & serializer_class ...
    


    def get_permissions(self):
        # 1. الحذف: للسوبر آدمن فقط
        if self.action == 'destroy':
            return [IsSectorAdminOrSuperAdmin()]
            
        # 2. التعديل (Update): للآدمن (بشرط نفس القطاع) وللسوبر آدمن
        elif self.action in ['update', 'partial_update']:
            return [IsSectorAdminOrSuperAdmin()]
            
        # 3. الإضافة (Create): للآدمن وللسوبر آدمن
        elif self.action == 'create':
            return [IsAdminOrSuperAdmin()]
            
        # 4. العرض (List): للآدمن وللسوبر آدمن
        return [IsAdminOrSuperAdmin()]