from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from .models import Meal
from .forms import MealForm
import requests
from django.utils.timezone import now, timedelta
from django.shortcuts import redirect
from django.contrib.auth import logout

# Fetch calories from USDA API (AJAX for frontend)
def fetch_calories(request):
    if request.method == "GET":
        food = request.GET.get("food", "").strip()
        quantity = float(request.GET.get("quantity", 0))
        unit = request.GET.get("unit", "grams").strip()

        if not food or quantity <= 0:
            return JsonResponse({"error": "Invalid food or quantity"}, status=400)

        API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
        API_KEY = "0glhCUFnJF0DCfy53vfAfBQnbQx6GhxpmFrfofrM"
        params = {"query": food, "api_key": API_KEY}

        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "foods" in data and data["foods"]:
                food_nutrients = data["foods"][0].get("foodNutrients", [])
                for nutrient in food_nutrients:
                    if nutrient.get("nutrientName") == "Energy" and nutrient.get("unitName") == "KCAL":
                        calories_per_100g = nutrient.get("value", 0)
                        calculated_calories = (calories_per_100g / 100) * quantity
                        return JsonResponse({"calories": round(calculated_calories, 2)})

                return JsonResponse({"error": "Calorie data not found"}, status=404)
            else:
                return JsonResponse({"error": "Food item not found"}, status=404)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"API request failed: {str(e)}"}, status=500)


# Fetch calories from USDA API (for backend usage in meal_entry function)
def fetch_calories_backend(food, quantity, unit):
    API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
    API_KEY = "0glhCUFnJF0DCfy53vfAfBQnbQx6GhxpmFrfofrM"
    params = {"query": food, "api_key": API_KEY}

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "foods" in data and data["foods"]:
            food_nutrients = data["foods"][0].get("foodNutrients", [])
            for nutrient in food_nutrients:
                if nutrient.get("nutrientName") == "Energy" and nutrient.get("unitName") == "KCAL":
                    calories_per_100g = nutrient.get("value", 0)
                    return round((calories_per_100g / 100) * quantity, 2)

        return 0.0  # Default to 0.0 if API fails
    except requests.exceptions.RequestException as e:
        print(f"USDA API request failed: {e}")
        return 0.0


# Register User
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})


# Meal Entry (Create & Edit)
@login_required
def meal_entry(request, meal_id=None):
    if meal_id:
        meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    else:
        meal = None

    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user

            # Fetch accurate calories based on entered quantity
            meal.calories = fetch_calories_backend(meal.food_item, meal.quantity, meal.unit)

            # Ensure calories are never NULL
            if meal.calories is None:
                meal.calories = 0.0

            meal.save()
            return redirect('meal_entry')

    else:
        form = MealForm(instance=meal)

    meals = Meal.objects.filter(user=request.user).order_by('-date')

    # Calculate total daily calories for each date
    total_calories = {}
    for meal in meals:
        total_calories.setdefault(meal.date, 0)
        total_calories[meal.date] += meal.calories

    return render(request, 'tracker/meal_entry.html', {'form': form, 'meals': meals, 'total_calories': total_calories})


# Delete Meal
@login_required
def delete_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    meal.delete()
    return redirect('meal_entry')


# Dashboard View (Home Page - Displays User Info Instead of Calories)
@login_required
def dashboard(request):
    user = request.user  #  Get logged-in user
    return render(request, 'tracker/dashboard.html', {'user': user})


@login_required
def weekly_dashboard(request):
    # Get the last 7 days' calorie data
    start_date = now().date() - timedelta(days=6)  # 7-day range
    end_date = now().date()

    # Ensure all last 7 days are included, even with no meals
    weekly_data = {str(start_date + timedelta(days=i)): 0 for i in range(7)}

    # Fetch meals from the last 7 days
    meals = Meal.objects.filter(user=request.user, date__range=[start_date, end_date])

    for meal in meals:
        meal_date = str(meal.date)  # Convert date to string for matching
        weekly_data[meal_date] += meal.calories  # Sum daily calories

    return render(request, 'tracker/weekly_dashboard.html', {'weekly_data': weekly_data})

def custom_logout(request):
    logout(request)
    return redirect('login')