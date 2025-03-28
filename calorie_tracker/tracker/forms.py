from django import forms
from .models import Meal, TDEECalculator

class MealForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Calendar Picker

    class Meta:
        model = Meal
        fields = ['date', 'meal_type', 'food_item', 'quantity', 'unit']

class TDEECalculatorForm(forms.ModelForm):
    class Meta:
        model = TDEECalculator
        fields = ['age', 'height', 'weight', 'gender', 'activity_level']
        widgets = {
            'gender': forms.Select(choices=[('male', 'Male'), ('female', 'Female')]),
            'activity_level': forms.Select(choices=TDEECalculator.ACTIVITY_LEVELS),
        }


from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
