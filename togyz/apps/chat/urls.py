from django.urls import path

from . import views

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('waiting_room', views.waiting_room, name='waiting_room'),
    path('test/', views.test, name='test'),
    path('<str:room_name>/', views.room, name='room'),
]
