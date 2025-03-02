from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Meal
from django.contrib.auth.models import User

# ✅ Unregister User first to avoid "AlreadyRegistered" error
admin.site.unregister(User)

# ✅ Custom User Admin Configuration
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('date_joined',)

# ✅ Re-register User with custom settings
admin.site.register(User, CustomUserAdmin)

# ✅ Register the Meal model for admin panel access
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'meal_type', 'food_item', 'quantity', 'unit', 'calories')
    search_fields = ('food_item', 'user__username')
    list_filter = ('meal_type', 'date')
    ordering = ('-date',)
    date_hierarchy = 'date'  # ✅ Adds a date-based filter in admin panel
