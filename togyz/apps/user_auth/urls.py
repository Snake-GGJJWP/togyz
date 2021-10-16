from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.registration_page, name='registration'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('test/<str:test>', views.test, name='test')
]
