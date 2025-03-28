from django.urls import path
from . import views
from .views import tdee_calculator
from .views import send_meal_notification
from .views import register


urlpatterns = [
    path('fetch_calories/', views.fetch_calories, name='fetch_calories'),  # ✅ Ensure this line is present
    path('meal_entry/', views.meal_entry, name='meal_entry'),
    path('meal_entry/<int:meal_id>/', views.meal_entry, name='edit_meal'),
    path('delete_meal/<int:meal_id>/', views.delete_meal, name='delete_meal'),
    path("send-meal-reminder/", send_meal_notification, name="send_meal_reminder"),
    path('weekly_dashboard/', views.weekly_dashboard, name='weekly_dashboard'),
    path('tdee_calculator/', tdee_calculator, name='tdee_calculator'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
]
