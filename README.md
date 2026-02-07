# Distinctiveness and Complexity:
My final project for CS50W is a calorie tracking application that provides personalized recommendations for calories. These recommendations are determined by the user's height, weight, age and activity level. To accurately estimate energy expenditure, I have utilized the 2023 Dietary Reference Intake. Once we have calculated the baseline expenditure, the user can then proceed to select their goals as well as their dietary preferences. 

The goals that the user can select from is to gain, lose or maintain weight. Each selection will then appropriately adjust the number of calories. While, offering a flexible rate would offer the greatest customizability for the scope of this project I decided to utilize rates that have been recommended by the papers.

The user can select a Balanced, Low-fat or Low-carb diets, each diet will then accordingly adjust the macronutrients to adhere to the selected dietary preferences. Finally, the user can select their preferred protein intake which ranges from low, moderate or high. This will then allocate the appropriate amount of protein based on the selection.  

After the user has completed this onboarding, they will be directed to the calorie tracker, this tracker consists of the user's target calories, proteins, fats and carbohydrates.

The calorie tracker records the calories and macronutrients for each day; the user can add foods to their daily log by clicking the add food card. Once they click this card, they will use a modal to search for the foods which dynamically generate results by fetching information as the user types on their keyboard. Once they find the food that they are looking for, the user can then click on the food. Once they click on the food the user can then select units and the quantity of foods which too will dynamically update the calories and macronutrients that are seen by the user. The units included are the typical units that you would expect to see for a given food, for example, eggs have the example of 1 large, grams and oz. Based on the units and quantity we appropriately calculate the calories and macronutrients for said food.

Once they select the appropriate units and quantity, they can add this food to their daily log which will update the respective progress bars to visually show the user how many calories, proteins, fats and carbohydrates they have consumed and how much they have left. Similarly, the user can also remove any foods from their daily log which will update the calories, proteins, fats and carbohydrates as well. The user can navigate forwards and backwards between dates as well which can let the user see their logs across time. It will also enable the application to display trends across time which is a potential expansion for the web application. Additionally, other areas for improvement could be to let users add custom foods or even potentially create recipes which allow for greater customizability. What’s currently missing from the application is the ability to edit their nutrition program which will be another feature that can be added to the application.

The complexity of the project arises as the user can select from a wide range of different food and portion sizes that dynamically update, each food has a different density so the conversion factors from various units is different as well. Each food has a different set of units which are loaded based on the food. These foods are then stored as a log when the wishes to add a food to his daily log. The daily log comprises of foodlogs. With regards to all the algorithms that are running on server side, they utilise scientifically published formulas. Additionally, instead of changing the url each time something occurs, to make the experience more seamless for the user, the search uses javascript to fetch results and it does so everytime the user types on the keyboard displaying the appropriate information. The subsequent food-detail modal also uses javascript to display the information of a food and then updates its values (calories, proteins, fats, and carbohydrates) when the user changes the quantity or units. 

# Structure 
tracker
├─ tracker
│  ├─ __pycache__
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ setting.py
│  ├─ urls.py
│  └─ wsgi.py
├─ calorie
│  ├─ __pycache__
│  ├─ migrations
│  ├─ templates
│  │  └─ calorie
│  │     ├─ entries.html
│  │     ├─ index.html
│  │     ├─ layout.html
│  │     ├─ login.html
│  │     ├─ questionnaire.html
│  │     ├─ register.html
│  │     └─ user.html
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ db.sqlite3
├─ manage.py
├─ README.md
└─ requirements.txt

The calorie folder shows the contents of the app

# Files
The project includes:
- README.md: which describes the project and the files contained in the project
- requirements.txt: lists the requirements for the project
- views.py consists of all the views that are utilised in the project.
    - index(request): is loaded when the user first opens the project, if the user has logged in they are directed to the user_view else they are directed to the 'calorie/index.html'
    - login_view(request): will try to log the user in, if successful it will redirect the user to the index. Else, it refreshes the 'calorie/login.html' with an error message
    - logout_view(request): logs the user out (only available if the user is signed in)
    - user_view(request): first checks if any get information has been provided, if provided it will load the daily log for that day else, loads date of today. The view then checks if the user has a nutrition profile, if it does then it will generate the "calorie/user.html" with the nutritional_profile information for the user (calories, fats, protein, etc), it then checks if the user has any logs associated with the dailyLog for the date,if it does, it provides the progress bar information and food entries otherwise it provides progress bar information with values of 0 and any empty list for the entries. If the user does not have a nutrition profile, they are directed to the 'calorie/questionnaire.html' where the user fills out forms to create a nutritional profile.
    - questionnaire(request): will try to gett he values posted from the form which will then be used to compute the nutritional profile for the individual using the scientific formulas depending on the user's gender, activity level, protein_preference and diet_preference. Once the profile has been created, they will be redirected to the user_view
    - register(request): lets the user register using the form on 'calorie/register.html'
    - search_foods(request): returns a list of foods from the database where the food's name contains the enter query
    - food_detail(request, food_id): returns a JsonResponse for a food with the corresponding food_id, it is used in the expanded food view modal.
    - log_food(request): expects a post method with a json object which contains information about the food, quantity, unit, date and then gets or creates a DailyLog exists with that date, after which it creates a logEntry which corresponds to that DailyLog. It then calls the function update_daily_log(daily_log) passing in the daily log. It then gets the nutrition profile and provides information for the progress bars.
    - update_daily_log(daily_log): gets all the entries for the dailylog and recomputes the calories, protein, fats and carbohydrates and updates the information for said daily_log. It then saves this information.
    - remove_log(request): receives information that is posted via a form. It provides the log_id, daily_log_id and target_date. It then tries to find the Log with log_id and delete it, gets the daily_log and updates it, and returns the user to the page user_view
- templates/calorie
    - entries.html: lists all the entries that are contained for a user for a given day (if has_log_entries), displays this list of entries in the user_view in the div block with id="meals"
    - index.html: A welcome page for not registered/signed-in users where the user is given the option to either login or register
    - layout.html: contains information for the navbar and relevant head files (bootstrap css and js)
    - login.html: The login page with a form to login
    - questionnaire.html: The questionnaire form which is used to create a nutrition profile, includes various questions like Height, weight, age, activity level, gender, goal, diet preference, protein preference
    - register.html: user can register via this html by entering an email and password
    - user.html: The main view for the application which the user uses to log foods against their target macronutrients and calories. They can add foods to their day, navigate to different pages, search for foods select their appropriate unit and quanity(handled by JS).
- models.py: The project contains 6 models in total
    - NutritionProfile: stores all the important information about the user including height, weight, etc. It uses this personal information to calculate the target_protein, target_fats, target_carbs and target_calories which are also stored in this model
    - Unit: consists of all the various units that a food can have (include teaspoon, tablespoon, etc)
    - Food: Stores relevant information about the food, using a base unit, base quantity and the relevant calories and macronutrients.
    - UnitConversion: Has a foreign key of food, which it then defines the relevant conversion for by entering the convert from unit to the convert to unit and then include the conversion in the conversion_factor (for example: converting water g to ml has conversion_factor 1)
    - LogEntry: includes a food, a daily_log to which it is associated with, quanity of food, unit of food, calories and macronutrients
    - DailyLog: which is associated with a user, and a date. Includes the total calories and macronutrients for a specific user on a specific day
- admin.py: Includes the models for which the admin can edit/add/delete details. Includes NutritionProfile, Unit, Food, UnitConversion, LogEntry and DailyLog
- urls.py 
    urlpatterns include:
    1. path("", views.index, name="index"), 
    2. path("login", views.login_view, name="login"),
    3. path("logout", views.logout_view, name="logout"),
    4. path("register", views.register, name="register"),
    5. path("user", views.user_view, name="user"),
    6. path("questionnaire", views.questionnaire, name='questionnaire'),
    7. path("search-foods", views.search_foods, name="search_foods"),
    8. path("food-details/<int:food_id>", views.food_details, name="food_details"),
    9. path("log-food",views.log_food, name="log_food" ),
    20. path("remove-log", views.remove_log, name="remove_log"),