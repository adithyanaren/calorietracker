from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard is home page
    path('register/', views.register, name='register'),
    path('meal_entry/', views.meal_entry, name='meal_entry'),
    path('meal_entry/<int:meal_id>/', views.meal_entry, name='edit_meal'),
    path('delete_meal/<int:meal_id>/', views.delete_meal, name='delete_meal'),
    path('fetch_calories/', views.fetch_calories, name='fetch_calories'),
    path('weekly_dashboard/', views.weekly_dashboard, name='weekly_dashboard'),

    # Correct login/logout paths
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
]
