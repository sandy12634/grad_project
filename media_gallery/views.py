from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Media
from .serializers import MediaSerializer
from .permissions import IsAdminOrReadOnly

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all().order_by('-created_at')
    serializer_class = MediaSerializer
    permission_classes = [IsAdminOrReadOnly]