from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins

from .models import User
from .serializers import UserSerializer


# Create your views here.

def index(request):
    pass

class UserViewSet(mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
