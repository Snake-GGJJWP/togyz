from django.urls import path

from .views import info

urlpatterns = [
    path('<str:lang>', info, name='info')
]
