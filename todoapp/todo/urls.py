from django.urls import path
from . import views
urlpatterns = [
    path('' , views.home , name='home'),
    path('login' , views.user_login , name='login'),
    path('logout' , views.user_logout , name='logout'),
    path('register' , views.user_register , name='register'),
    path('toggle/<int:pk>/', views.toggle_task, name='toggle-task'),
    path('delete/<int:pk>/', views.delete_task, name='delete-task'),
    path('edit/<int:pk>/', views.edit_task, name='edit-task'),

]