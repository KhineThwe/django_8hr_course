from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage,name='login'),
    path('logout/', views.logoutUser,name='logout'),
    path('register/', views.registerPage,name='register'),
    path('', views.home,name='home'),
    path('create_room/', views.create_room,name='create_room'),
    path('room/<int:pk>/', views.room,name='room'),
    path('update_room/<int:pk>/', views.update_room,name='update_room'),
    path('delete_room/<int:pk>/', views.delete_room,name='delete_room'),
    path('delete_message/<int:pk>/', views.delete_message,name='delete_message'),
]
