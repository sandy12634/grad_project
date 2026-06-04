from rest_framework import serializers
from .models import Inquiry

class InquirySerializer(serializers.ModelSerializer):
    
    sector_display=serializers.CharField(source='get_sector_display',read_only=True)
    
    
    class Meta:
        model = Inquiry
        fields = ['id', 'name', 'sector','sector_display', 'question', 'answer','status','created_at']