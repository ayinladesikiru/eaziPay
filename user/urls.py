from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProfileViewSet

router = DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')


urlpatterns = router.urls