from django.contrib import admin
from django.urls import path
from .views import Home, logoutuser,signupuser, feed, add, edit, delete, download_file
urlpatterns = [
    path('', Home, name='Home'),
    path('logout/', logoutuser, name='logout'),
    path('signup/', signupuser, name='signupuser'),
    path('feed/', feed, name='feed'),
    path('feed/add_file/', add, name='add_file'),
    path('feed/view_file/<uuid:pk>/', edit, name='viewfile'),
    path('feed/delete_file/<uuid:pk>/', delete, name='deletefile'),
    path('feed/download/<uuid:pk>/', download_file, name='download')

]