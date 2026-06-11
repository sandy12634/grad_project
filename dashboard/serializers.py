from rest_framework import serializers
from .models import MonthlyStat, SectorStat

class MonthlyStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyStat
        fields = ['month', 'month_en', 'news', 'events', 'services', 'facilities']

class SectorStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectorStat
        fields = ['sector', 'news', 'events', 'services', 'facilities']