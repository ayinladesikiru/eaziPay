from requests import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from .models import Profile, User
from .serializers import ProfileSerializer, DashBoardSerializer


# Create your views here.

class ProfileViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer


    def get_queryset(self):
        try:
            return Profile.objects.filter(user=self.request.user)
        except Profile.DoesNotExist:
            return Profile.objects.none()

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]


class DashBoardView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DashBoardSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)