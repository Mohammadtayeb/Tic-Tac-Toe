from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('message', views.message, name='message'),
    path('log_in', views.log_in, name='log_in'),
    path('log_out', views.log_out, name='log_out'),
    path('change_password', views.change_password, name='change_password'),
    path('enter', views.enter, name='enter'),
    path('create_room', views.create_room, name='create_room'),
    path('join_room', views.join_room, name='join_room'),
    path('room', views.room, name='room'),
    path('is_joined', views.is_joined, name='is_joined'),
    path('cur_usr', views.cur_usr, name='cur_usr'),
    path('computer', views.computer, name='computer'),
    path('about_contact', views.about_contact, name='about_contact'),
    path('delete_current_connection', views.delete_current_connection, name='delete_current_connection')
]