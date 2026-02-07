import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime



from .models import NutritionProfile, User, Food, UnitConversion, DailyLog, LogEntry
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user"))
    return render(request, "calorie/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "calorie/login.html", {
                "message": "Invalid Login Credentials"
            }) 
    return render(request, "calorie/login.html")  

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def user_view(request):
    date_str = request.GET.get("date")
    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()   
        except ValueError:
            target_date = now().date()
    else:
        target_date = now().date()

    has_nutrition_profile = NutritionProfile.objects.filter(user=request.user).exists()
    if has_nutrition_profile:
        nutrition_profile = NutritionProfile.objects.get(user=request.user)
        daily_log = DailyLog.objects.filter(user=request.user, date=target_date).first()
        if not daily_log:
            return render(request, "calorie/user.html", {
            "profile": nutrition_profile,
            "has_log_entries": False,
            "daily_log": None,
            "entries": [],
            "percentage_calories": 0,
            "date": target_date
        })

        has_log_entries = LogEntry.objects.filter(daily_log=daily_log).exists()
        if (has_log_entries):
            log_entry = LogEntry.objects.filter(daily_log=daily_log).order_by("-created_at")
            percentage_calories = daily_log.calories / nutrition_profile.target_calories *100
            percentage_protein = daily_log.protein / nutrition_profile.target_protein * 100
            percentage_carbs = daily_log.carbs / nutrition_profile.target_carbs * 100
            percentage_fats = daily_log.fats / nutrition_profile.target_fats * 100
        else:
            log_entry = []
            percentage_calories = 0
            percentage_protein = 0
            percentage_carbs = 0
            percentage_fats = 0

        entries = [entry for entry in log_entry]
        return render(request, "calorie/user.html", {
            "profile": nutrition_profile,
            "has_log_entries": has_log_entries,
            "daily_log": daily_log,
            "entries": entries,
            "percentage_calories": percentage_calories,
            "percentage_protein": percentage_protein,
            "percentage_carbs": percentage_carbs,
            "percentage_fats": percentage_fats,
            "date": target_date
        })
    else:
        return render(request, "calorie/questionnaire.html")

@login_required
def questionnaire(request):
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        height = request.POST["height"]
        weight = request.POST["weight"]
        age = request.POST["age"]
        gender = request.POST["gender"]
        activity_level = request.POST["activity-level"]
        goal = request.POST["goal"]
        diet_pref = request.POST["diet-pref"]
        protein_pref = request.POST["protein-pref"]
        
        if gender == "male":
            if activity_level == "sedentary":
                bmr = 753.07 - (10.83 * float(age)) + (6.50 * float(height)) + (14.10 * float(weight))
            elif activity_level == "moderate":
                bmr = 581.47 - (10.83 * float(age)) + (8.30 * float(height)) + (14.94 * float(weight))
            elif activity_level == "active":
                bmr = 1004.82 - (10.83 * float(age)) + (6.52 * float(height)) + (15.91 * float(weight))
            else:
                bmr = -517.88 - (10.83 * float(age)) + (15.61 * float(height)) + (19.11 * float(weight))
        else: 
            if activity_level == "sedentary":
                bmr = 584.90 - (7.01 * float(age)) + (5.72 * float(height)) + (11.71 * float(weight))
            elif activity_level == "moderate":
                bmr = 575.77 - (7.01 * float(age)) + (6.60 * float(height)) + (12.14 * float(weight))
            elif activity_level == "active":
                bmr = 710.25 - (7.01 * float(age)) + (6.54 * float(height)) + (12.34 * float(weight))
            else:
                bmr = 511.83 - (7.01 * float(age)) + (9.07 * float(height)) + (12.56 * float(weight))
        
        if goal == "bulk":
            # Assumes a rate of 0.025% weight gain per week which is then converted to calories. We can then calculate the daily calories based on this calculation by dividing by 7
            target_calories = (bmr*7 + (0.0025*float(weight)*7716.179176))/7
        elif goal == "cut":
            # Assumes a rate of 0.05% weight loss per week which is then converted to calories. We can then calculate the daily calories based on this calculation by dividing by 7
            target_calories = (bmr*7 - (0.005*float(weight)*7716.179176))/7
        else:
            target_calories = bmr

        if protein_pref == "low":
            target_protein = int(1.76 * float(weight))
        elif protein_pref == "moderate":
            target_protein = int(1.98 * float(weight))
        else:
            target_protein = int(2.20 * float(weight))
        
        if diet_pref == "balanced":
            target_carbohydrates = int((target_calories * 0.55)/4)
            target_fats = int((target_calories - (target_protein * 4) - (target_carbohydrates *4))/9)
        elif diet_pref == "low-fat":
            target_fats = int((target_calories * 0.20)/9)
            target_carbohydrates = int((target_calories - (target_fats)*9 - (target_protein*4))/4)
        else:
            target_carbohydrates = 130
            target_fats = int((target_calories - (target_carbohydrates * 4) - (target_protein * 4))/9)
        
        nutrition_profile, created = NutritionProfile.objects.get_or_create(
            user=user,
            height=height,
            weight=weight,
            age=age,
            goal=goal,
            diet_preference=diet_pref,
            protein_preference=protein_pref,
            bmr=bmr,
            target_calories=int(target_calories),
            target_protein=target_protein,
            target_carbs=target_carbohydrates,
            target_fats=target_fats
            )
        
        return HttpResponseRedirect(reverse("user"))
    
    has_nutrition_profile = NutritionProfile.objects.filter(user=request.user).exists()
    if has_nutrition_profile:
        return HttpResponseRedirect(reverse("user"))
    else: 
        return render(request, "calorie/questionnaire.html")
    
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "calorie/register.html", {
                "message": "Passwords must match"
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "calorie/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "calorie/register.html")

def search_foods(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        foods = Food.objects.filter(name__icontains=query)
        for food in foods:
            results.append({
                "id": food.id,
                "name": food.name,
                "calories": food.calories,
                "protein": food.protein,
                "carbs": food.carbs,
                "fats": food.fats,
            })

    return JsonResponse({"results": results})

@login_required
def food_details(request, food_id):

    try:
        food = Food.objects.get(pk=food_id)
    except Food.DoesNotExist:
        return JsonResponse({"error": "Food does not exist"})
    
    unit_conversions = UnitConversion.objects.filter(food=food)
    conversions = [
        {"from": unit.from_unit.abbreviation,
         "to": unit.to_unit.abbreviation,
         "factor": unit.factor
        }
        for unit in unit_conversions
    ]
    units = [
        {   
            "id": unit.from_unit.id,
            "abbreviation": unit.from_unit.abbreviation
        }
        for unit in unit_conversions
        ]


    return JsonResponse({
        "id": food.id,
        "name": food.name,
        "calories": food.calories,
        "protein": food.protein,
        "carbs": food.carbs,
        "fats": food.fats,
        "units":units,
        "conversions": conversions,
        "base_unit": food.base_unit.abbreviation
    })


@login_required
def log_food(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    try:
        food = Food.objects.get(pk=data["food_id"])
    except Food.DoesNotExist:
        return JsonResponse({"error": "Food does not exist"})
    
    quantity = float(data["quantity"])
    unit = data["unit"]

    calories = data["calories"]
    protein = data["protein"]
    fats = data["fats"]
    carbs = data["carbs"]
    date = data["date"]

    target_date = datetime.strptime(date, "%Y-%m-%d").date()

    daily_log, created = DailyLog.objects.get_or_create(user=request.user, date=target_date)

    log_entry = LogEntry(
        food=food,
        daily_log=daily_log,
        quantity=quantity,
        unit=unit,
        calories=calories,
        protein=protein,
        fats=fats,
        carbs=carbs
    )

    log_entry.save()

    update_daily_log(daily_log=daily_log)

    nutrition_profile = NutritionProfile.objects.get(user=request.user)

    percentage_calories = daily_log.calories / nutrition_profile.target_calories *100
    percentage_protein = daily_log.protein / nutrition_profile.target_protein * 100
    percentage_carbs = daily_log.carbs / nutrition_profile.target_carbs * 100
    percentage_fats = daily_log.fats / nutrition_profile.target_fats * 100

    return JsonResponse({
        "entry": {
            "id": log_entry.id,
            "food_name": food.name,
            "quantity": quantity,
            "unit": unit,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fats": fats
        },
        "daily_log": {
            "calories": daily_log.calories,
            "protein": daily_log.protein,
            "carbs": daily_log.carbs,
            "fats": daily_log.fats
        },
        "percentages": {
            "calories": percentage_calories,
            "protein": percentage_protein,
            "carbs": percentage_carbs,
            "fats": percentage_fats
        },
        "nutrition_profile": {
            "target_calories": nutrition_profile.target_calories,
            "target_protein": nutrition_profile.target_protein,
            "target_carbs": nutrition_profile.target_carbs,
            "target_fats": nutrition_profile.target_fats
        }
    })

def update_daily_log(daily_log):
    entries = daily_log.entries.all()

    daily_log.calories = sum(entry.calories for entry in entries)
    daily_log.protein = sum(entry.protein for entry in entries)
    daily_log.carbs = sum(entry.carbs for entry in entries)
    daily_log.fats = sum(entry.fats for entry in entries)

    daily_log.save()

@login_required
def remove_log(request):
    if request.method != "POST":
        return JsonResponse({"error": "Must be post"})
    
    log_id = request.POST["log_id"]
    daily_log_id = request.POST["daily_log_id"]
    target_date = request.POST["daily_log_date"]
    try:
        LogEntry.objects.filter(pk=log_id).delete()
        daily_log = DailyLog.objects.get(pk=daily_log_id) 
        update_daily_log(daily_log)
        return HttpResponseRedirect(f"{reverse('user')}?date={target_date}")
    
    except LogEntry.DoesNotExist:
        return render(request, "calorie/user.html",{
            "message": "Log does not exist"
            })
    except DailyLog.DoesNotExist:
        return render(request, "calorie/user.html",{
            "message": "Daily Log does not exist"
            })
    