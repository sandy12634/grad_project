from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """تخصيص البيانات العائدة عند تسجيل الدخول لتشمل تفاصيل الدور والقطاع"""
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # إضافة بيانات المستخدم المخصصة للرد (Response)
        # تساعد هذه البيانات الفرونت إند في معرفة صلاحيات المستخدم فوراً
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'full_name': f"{self.user.first_name} {self.user.last_name}".strip(),
            'role': self.user.role,
            'sector': self.user.sector,
        }
        return data

class UserSerializer(serializers.ModelSerializer):
    """سيريالايزر لإدارة بيانات الأدمن والسوبر أدمن"""
    # جعل كلمة السر للكتابة فقط لزيادة الأمان
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'sector', 'password']

    def create(self, validated_data):
        """تشفير كلمة السر عند إنشاء مستخدم (أدمن) جديد"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password) # تشفير الباسورد
        user.save()
        return user

    def update(self, instance, validated_data):
        """تشفير كلمة السر في حال تم تعديلها أثناء التحديث"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def validate_sector(self, value):
        """منع الأدمن من محاولة إضافة شخص في قطاع غير قطاعه"""
        user = self.context['request'].user
        if user.role == 'admin' and value != user.sector:
            raise serializers.ValidationError("لا يمكنك إضافة أو تعديل مستخدم خارج قطاعك.")
        return value
    
    
