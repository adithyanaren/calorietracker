from django import forms
from .models import Meal


class MealForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Calendar Picker

    class Meta:
        model = Meal
        fields = ['date', 'meal_type', 'food_item', 'quantity', 'unit']
