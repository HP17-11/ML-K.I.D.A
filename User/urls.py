from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.loginUser, name='loginUser'),
    path('register/', views.createUser, name='createUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),

    path('profile/', views.user_profile, name='profile'),
    path('ownersprofile/<str:pk>/', views.owners_profile, name='ownersprofile'),


]