from django.contrib.auth.models import User
from django.db import models

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snack', 'Snack'),
        ('dinner', 'Dinner'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    food_item = models.CharField(max_length=200)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20, choices=[('grams', 'Grams'), ('ml', 'Milliliters')])
    calories = models.FloatField()

    class Meta:
        unique_together = ('user', 'date', 'meal_type', 'food_item')

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.meal_type} - {self.food_item}"
