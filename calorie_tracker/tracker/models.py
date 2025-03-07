from django.contrib.auth.models import User
from django.db import models

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snack', 'Snack'),
        ('dinner', 'Dinner'),
    ]

    UNIT_CHOICES = [
        ('grams', 'Grams'),
        ('ml', 'Milliliters'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    food_item = models.CharField(max_length=200)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    calories = models.FloatField(default=0.0)

    # Macronutrients
    protein = models.FloatField(default=0.0)
    carbs = models.FloatField(default=0.0)
    fat = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'date', 'meal_type', 'food_item')

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.meal_type} - {self.food_item}"

class TDEECalculator(models.Model):
    ACTIVITY_LEVELS = [
        ('sedentary', 'Sedentary (little to no exercise)'),
        ('light', 'Light (1-3 days of exercise)'),
        ('moderate', 'Moderate (3-5 days of exercise)'),
        ('active', 'Active (6-7 days of exercise)'),
        ('very_active', 'Very Active (twice per day training)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=18)  # ✅ Prevent NULL errors
    height = models.FloatField(default=170.0)  # ✅ Default height in cm
    weight = models.FloatField(default=70.0)  # ✅ Default weight in kg
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], default='male')
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVELS, default='moderate')
    tdee = models.FloatField(blank=True, null=True)

    def calculate_tdee(self):
        """Calculates Total Daily Energy Expenditure (TDEE)"""
        if self.gender == 'male':
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        self.tdee = bmr * activity_multipliers[self.activity_level]
        return self.tdee
