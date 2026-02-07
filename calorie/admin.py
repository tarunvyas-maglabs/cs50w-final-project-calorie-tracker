from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(NutritionProfile)
admin.site.register(Food)
admin.site.register(Unit)
admin.site.register(UnitConversion)
admin.site.register(DailyLog)
admin.site.register(LogEntry)