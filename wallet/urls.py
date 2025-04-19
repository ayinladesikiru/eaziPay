from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('greet/<str:name>', views.greeting, name='greet'),
    path('fund/account', views.fund_wallet, name='fund_wallet'),
]