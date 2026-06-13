from rest_framework import viewsets
from .premissions import IsSuperAdmin, IsAdminOrSuperAdmin, IsSectorAdminOrSuperAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": "بيانات الدخول غير صحيحة"}, status=status.HTTP_400_BAD_REQUEST)
        
        # هون السحر! عم ناخد الداتا المفلترة والمعدلة من السيريالايزر
        generated_data = serializer.validated_data
        
        # بنصنع الـ Response الافتراضي (عشان الكوكيز تضل شغال في الخلفية للأمان)
        response = Response(generated_data, status=status.HTTP_200_OK)
        
        # وبنأكد إن التوكنات انكتبت غصب عنها جوات الـ JSON Body اللي هيشوفه بشار بالـ JavaScript
        response.data['access'] = generated_data.get('access')
        response.data['refresh'] = generated_data.get('refresh')
        response.data['accessToken'] = generated_data.get('access') # احتياطاً إذا بشار عم يدور على هاد الاسم
        
        return response
    
    
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
        return [AllowAny()]