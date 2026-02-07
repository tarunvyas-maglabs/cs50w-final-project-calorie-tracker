from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

# Create your models here.

class NutritionProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nutrition")
    height = models.IntegerField()
    weight = models.FloatField()
    age = models.IntegerField()
    goal = models.CharField()
    diet_preference = models.CharField()
    protein_preference = models.CharField()

    bmr = models.IntegerField()
    target_calories = models.IntegerField()
    target_protein = models.IntegerField()
    target_carbs = models.IntegerField()
    target_fats = models.IntegerField()

class Unit(models.Model):
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return self.abbreviation
    
class Food(models.Model):
    name= models.CharField()

    base_unit = models.ForeignKey(Unit,on_delete=models.PROTECT, related_name="base_foods")
    base_quantity = models.FloatField(default=100)

    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
     
    def __str__(self):
        return self.name
    
class UnitConversion(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="unit_conversions")

    from_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="from_conversions")
    to_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="toconversions")

    factor = models.FloatField()

    def __str__(self):
        return f" Convert {self.food.name} from {self.from_unit.abbreviation} to {self.to_unit.abbreviation}"

class LogEntry(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    daily_log = models.ForeignKey("DailyLog", on_delete=models.CASCADE, related_name="entries")
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    calories = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    carbs = models.FloatField()
    created_at = models.DateTimeField(default=now)


class DailyLog(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.PROTECT, related_name="daily_logs")
    date = models.DateField(default=now)
    calories = models.FloatField(default=0.0)
    protein = models.FloatField(default=0.0)
    carbs = models.FloatField(default=0.0)
    fats = models.FloatField(default=0.0)