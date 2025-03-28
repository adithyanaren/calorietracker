from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
import requests
from django.utils.timezone import now, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Meal, TDEECalculator
from .forms import MealForm, TDEECalculatorForm
from django.utils.timezone import now, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TDEECalculator
from .forms import TDEECalculatorForm
from django.http import JsonResponse
from .sns_utils import send_meal_reminder


# ✅ Custom Login View (Prevents Authenticated Users from Accessing Login Page)
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect if already logged in

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# ✅ Fetch Calories & Macronutrients from USDA API (AJAX)
def fetch_calories(request):
    if request.method == "GET":
        food = request.GET.get("food", "").strip()
        quantity = float(request.GET.get("quantity", 0))
        unit = request.GET.get("unit", "grams").strip()

        if not food or quantity <= 0:
            return JsonResponse({"error": "Invalid food or quantity"}, status=400)

        nutrients = fetch_nutrients_backend(food, quantity, unit)
        return JsonResponse(nutrients)

# ✅ Backend Function to Fetch Nutrients
def fetch_nutrients_backend(food, quantity, unit):
    API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
    API_KEY = "0glhCUFnJF0DCfy53vfAfBQnbQx6GhxpmFrfofrM"
    params = {"query": food, "api_key": API_KEY}

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "foods" in data and data["foods"]:
            nutrients = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
            food_nutrients = data["foods"][0].get("foodNutrients", [])

            for nutrient in food_nutrients:
                name = nutrient.get("nutrientName", "").lower()
                value = float(nutrient.get("value", 0))

                if "energy" in name and "kcal" in nutrient.get("unitName", "").lower():
                    nutrients["calories"] = round((value / 100) * quantity, 2)
                elif "protein" in name:
                    nutrients["protein"] = round((value / 100) * quantity, 2)
                elif "carbohydrate" in name:
                    nutrients["carbs"] = round((value / 100) * quantity, 2)
                elif "fat" in name:
                    nutrients["fat"] = round((value / 100) * quantity, 2)

            return nutrients

        return {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    except requests.exceptions.RequestException as e:
        print(f"USDA API request failed: {e}")
        return {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}

# ✅ Meal Entry (Ensures Meals Are User-Specific)
@login_required
def meal_entry(request, meal_id=None):
    meal = get_object_or_404(Meal, id=meal_id, user=request.user) if meal_id else None
    fetched_nutrients = None  # Stores fetched values for display

    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user

            # ✅ Fetch Macronutrients
            fetched_nutrients = fetch_nutrients_backend(meal.food_item, meal.quantity, meal.unit)
            meal.calories = fetched_nutrients.get("calories", 0.0)
            meal.protein = fetched_nutrients.get("protein", 0.0)
            meal.carbs = fetched_nutrients.get("carbs", 0.0)
            meal.fat = fetched_nutrients.get("fat", 0.0)

            meal.save()
            return redirect('meal_entry')

    else:
        form = MealForm(instance=meal)

    # ✅ Fetch only meals that belong to the logged-in user
    meals = Meal.objects.filter(user=request.user).order_by('-date')
    total_calories = {meal.date: 0 for meal in meals}

    for meal in meals:
        total_calories[meal.date] += meal.calories

    return render(request, 'tracker/meal_entry.html', {
        'form': form,
        'meals': meals,
        'total_calories': total_calories,
        'fetched_nutrients': fetched_nutrients  # ✅ Pass fetched values to the template
    })

# ✅ Delete Meal (Ensures Only Logged-in User Can Delete Their Own Meals)
@login_required
def delete_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    meal.delete()
    return redirect('meal_entry')

# ✅ Dashboard View
@login_required
def dashboard(request):
    return render(request, 'tracker/dashboard.html', {'user': request.user})

# ✅ Weekly Dashboard (Ensures User-Specific Data)
@login_required
def weekly_dashboard(request):
    start_date = now().date() - timedelta(days=6)
    end_date = now().date()

    weekly_data = {
        str(start_date + timedelta(days=i)): {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        for i in range(7)
    }

    meals = Meal.objects.filter(user=request.user, date__range=[start_date, end_date])

    for meal in meals:
        meal_date = str(meal.date)
        if meal_date in weekly_data:
            weekly_data[meal_date]["calories"] += meal.calories
            weekly_data[meal_date]["protein"] += meal.protein
            weekly_data[meal_date]["carbs"] += meal.carbs
            weekly_data[meal_date]["fat"] += meal.fat

    return render(request, 'tracker/weekly_dashboard.html', {'weekly_data': weekly_data})


@login_required
def tdee_calculator(request):
    """Handles TDEE calculation and form submission"""

    # ✅ Ensure we get an instance or None instead of creating an invalid entry
    tdee_instance = TDEECalculator.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = TDEECalculatorForm(request.POST, instance=tdee_instance)
        if form.is_valid():
            tdee_instance = form.save(commit=False)
            tdee_instance.user = request.user
            tdee_instance.calculate_tdee()
            tdee_instance.save()
            return redirect('tdee_calculator')  # Reload to display result

    else:
        form = TDEECalculatorForm(instance=tdee_instance)

    return render(request, 'tracker/tdee_calculator.html',
                  {'form': form, 'tdee': tdee_instance.tdee if tdee_instance else None})


# ✅ Custom Logout
def custom_logout(request):
    logout(request)
    return redirect('login')

def send_meal_notification(request):
    if request.method == "POST":
        response = send_meal_reminder()
        return JsonResponse({"message": "Meal reminder sent!", "sns_response": response})


from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # Inactive until admin approval
            user.save()
            messages.success(request, 'Account created! Await admin approval.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
