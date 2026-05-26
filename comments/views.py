from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Inquiry
from .serializers import InquirySerializer
from .permissions import IsSuperAdminOnly
from rest_framework import generics

class InquiryViewSet(generics.ListCreateAPIView):
    queryset = Inquiry.objects.all().order_by("-id")
    serializer_class = InquirySerializer

    permission_classes = [IsSuperAdminOnly]