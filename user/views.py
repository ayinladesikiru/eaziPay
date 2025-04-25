from requests import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from .models import Profile
from .serializers import ProfileSerializer


# Create your views here.

class ProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
        # return get_object_or_404(Profile, user__id=self.request.user.id)