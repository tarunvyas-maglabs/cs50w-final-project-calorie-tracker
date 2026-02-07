from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user", views.user_view, name="user"),
    path("questionnaire", views.questionnaire, name='questionnaire'),
    path("search-foods", views.search_foods, name="search_foods"),
    path("food-details/<int:food_id>", views.food_details, name="food_details"),
    path("log-food",views.log_food, name="log_food" ),
    path("remove-log", views.remove_log, name="remove_log"),
]