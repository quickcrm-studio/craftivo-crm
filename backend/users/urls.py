from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_management, name='user_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('management/', views.user_management, name='user_management'),
    path('management/create/', views.user_create, name='user_create'),
    path('management/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('management/delete/<int:pk>/', views.user_delete, name='user_delete'),
] 