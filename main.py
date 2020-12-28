# -------------------------------------------------------
# -------------------------------------------------------
# Workout Tracker App
import requests
import os
from datetime import datetime

now = datetime.now()
current_date = now.strftime("%d/%m/%Y")
current_time = now.strftime("%H:%M:%S")

nutritionix_APIKey = os.environ["NUTRITIONIX_APIKEY"]
nutritionix_AppID = os.environ["NUTRITIONIX_APPID"]


post_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": nutritionix_AppID,
    "x-app-key": nutritionix_APIKey
}

request_body = {
    "query": "Run 10 miles" # input("What activity(s) did you do: ").lower(),
    # "gender": input("What's your gender (male/female): ").lower(),
    # "weight": float(input("Enter your weight (Kg): ")),
    # "height": float(input("Enter your height (cm): ")),
    # "age": int(input("What age are you: "))
}

response = requests.post(url=post_endpoint, json=request_body, headers=headers)
response.raise_for_status()
json_data = response.json()
exercise_data = json_data["exercises"]
print(exercise_data)

sheety_post_endpoint = "https://api.sheety.co/2e22d7be903560b0d1d0aa06e5139fec/myWorkoutsV1/workouts"

SHEETY_AUTH_TOKEN = os.environ["SHEETY_AUTH_TOKEN"]

headers = {
    "Authorization": SHEETY_AUTH_TOKEN
}

# Load exercise data
for exercise_entry in exercise_data:
    exercise = exercise_entry["user_input"]
    duration = exercise_entry["duration_min"]
    calories = exercise_entry["nf_calories"]

    request_body = {
        "workout": {
            "date": current_date,
            "time": current_time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }

    # Load new row to google sheet
    response = requests.post(url=sheety_post_endpoint, json=request_body, headers=headers)
    print(response.json())