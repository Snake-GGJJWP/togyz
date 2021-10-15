from django.urls import path

from . import views

urlpatterns = [
    path('', views.lobby, name='lobby'),
    path('test/', views.test, name='test'),
    path('<str:room_name>/<str:color>/', views.room, name='room'),
]
