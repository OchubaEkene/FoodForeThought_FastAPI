from fastapi import FastAPI
import generate_mealplan as mp
import json

app = FastAPI()

# # Mount the static directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/get_mealplan/")
def getMealPlan(tribe: str, state: str, age: int, gender:str):
    """
    Get a 14-day Meal Plan with Breakfast, Lunch, and Dinner for each day.

    This API endpoint generates a meal plan for 14 days, where each day includes arrays for breakfast, lunch, and dinner. The response provides meal details including meal name, food category, calorie intake, meal measurement, and human-equivalent measurement.

    **Endpoint:**
    `GET /get_mealplan/`

    **Query Parameters:**

    - `tribe` (string, required): Specifies the tribe or cultural background to tailor the meal plan.
    - `state` (string, required): Specifies the state or region to adapt the meal plan according to local preferences.
    - `age` (integer, required): Specifies the age of the individual for appropriate meal planning.
    - `gender` (string, required): Specifies the gender of the individual for meal customization.

    **Request Example:**

    ```
    GET /get_mealplan/?tribe=Navajo&state=Arizona&age=30&gender=male
    ```

    **Response:**

    The response is a JSON object containing the `meal_plan` for 14 days. Each day is represented by an array of meals where index 0 is breakfast, index 1 is lunch, and index 2 is dinner.

    **Response Example:**

    ```json
    {
    "meal_plan": {
        "days": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        "meals": [
        [
            {
            "meal_name": "Oatmeal with Fruits",
            "food_category": "Breakfast",
            "calories_meal_intake": 350,
            "meal_measure_gram": 200,
            "human_equivalent_alternative_measure": "1 bowl"
            },
            {
            "meal_name": "Grilled Chicken Salad",
            "food_category": "Lunch",
            "calories_meal_intake": 500,
            "meal_measure_gram": 250,
            "human_equivalent_alternative_measure": "1 plate"
            },
            {
            "meal_name": "Baked Salmon with Veggies",
            "food_category": "Dinner",
            "calories_meal_intake": 600,
            "meal_measure_gram": 300,
            "human_equivalent_alternative_measure": "1 serving"
            }
        ],
        [
            {
            "meal_name": "Greek Yogurt with Honey",
            "food_category": "Breakfast",
            "calories_meal_intake": 250,
            "meal_measure_gram": 150,
            "human_equivalent_alternative_measure": "1 cup"
            },
            {
            "meal_name": "Turkey Sandwich",
            "food_category": "Lunch",
            "calories_meal_intake": 450,
            "meal_measure_gram": 200,
            "human_equivalent_alternative_measure": "1 sandwich"
            },
            {
            "meal_name": "Vegetable Stir-fry",
            "food_category": "Dinner",
            "calories_meal_intake": 550,
            "meal_measure_gram": 300,
            "human_equivalent_alternative_measure": "1 bowl"
            }
        ],
        // ... More days up to 14
        ]
    }
    }
    ```

    **Code Usage:**

    To use this endpoint in your code, you can make a GET request to `/get_mealplan/` with the necessary query parameters. Here's an example using Python's `requests` library:

    ```python
    import requests

    # Define the query parameters
    params = {
        'tribe': 'Navajo',
        'state': 'Arizona',
        'age': 30,
        'gender': 'male'
    }

    # Make the GET request
    response = requests.get('https://your-api-url.com/get_mealplan/', params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        meal_plan = response.json()
        print(meal_plan)
    else:
        print(f"Error: {response.status_code} - {response.text}")
    ```

    This example demonstrates how to query the API and handle the response to get a structured meal plan for 14 days.
    """

    try:
        results = mp.createMealPlan(tribe, state, age, gender)
        return results
    except Exception as e:
        print(f"{e}")
        raise e
    

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app)
