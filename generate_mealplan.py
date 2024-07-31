import openai
import json

with open('config.json', 'r') as keys:
    secret_keys = json.load(keys)

# Set your OpenAI API key from the config file
openai.api_key = secret_keys["openai_api_key"]

def generate_mealplan():
    pass

meal_plan_format = {}
day_list = []

for day in range(0, 31):
    day_list.append(f'day_{day + 1}')
    meal_plan_format[f'day_{day + 1}'] = {
        "type": "object",
        "description": f"Provide a meal plan for day {day + 1}'s meal breakdown for breakfast, lunch, and dinner. Include note on possible meal substitutions if necessary.",
        "properties": {
            "breakfast": {
                "type": "object",
                "description": f"Decide the meal will be eaten for breakfast on day {day + 1}",
                "properties": {
                    "food_name": {
                        "type": "string",
                        "description": "Give a descriptive name for the meal/ dish/ snack."
                    },
                    "food_category": {
                        "type": "string",
                        "description": "This meal can either be a light or heavy meal. this is to be decided as recommended by a professional dietitian."
                    },
                    "calories": {
                        "type": "number",
                        "description": "Calculate the calorie intake for this meal as a professional dietatian would."
                    },
                    "measure_gram": {
                        "type": "number",
                        "description": "Give the appropriate measure/ quantity recommended for this meal (given the client/patient's specs). Meal for the given calorie intake should be measured in grams."
                    },
                    "alternative_measure": {
                        "type": "string",
                        "description": "Return a human equivalent measurement for the meal and given calories (given that gram might be hard to quantify for people without scales at home)."
                    }
                },  # end of breakfast schedule
            },  # meal
            "lunch": {
                "type": "object",
                "description": f"Decide the meal will be eaten for lunch on day {day + 1}",
                "properties": {
                    "food_name": {
                        "type": "string",
                        "description": "Give a descriptive name for the meal/ dish/ snack."
                    },
                    "food_category": {
                        "type": "string",
                        "description": "This meal can either be a light or heavy meal. this is to be decided as recommended by a professional dietitian."
                    },
                    "calories": {
                        "type": "number",
                        "description": "Calculate the calorie intake for this meal as a professional dietatian would."
                    },
                    "measure_gram": {
                        "type": "number",
                        "description": "Give the appropriate measure/ quantity recommended for this meal (given the client/patient's specs). Meal for the given calorie intake should be measured in grams."
                    },
                    "alternative_measure": {
                        "type": "string",
                        "description": "Return a human equivalent measurement for the meal and given calories (given that gram might be hard to quantify for people without scales at home)."
                    }
                },  # end of lunch schedule
            },  # meal
            "dinner": {
                "type": "object",
                "description": f"Decide the meal will be eaten for dinner on day {day + 1}",
                "properties": {
                    "food_name": {
                        "type": "string",
                        "description": "Give a descriptive name for the meal/ dish/ snack."
                    },
                    "food_category": {
                        "type": "string",
                        "description": "This meal can either be a light or heavy meal. this is to be decided as recommended by a professional dietitian."
                    },
                    "calories": {
                        "type": "number",
                        "description": "Calculate the calorie intake for this meal as a professional dietatian would."
                    },
                    "measure_gram": {
                        "type": "number",
                        "description": "Give the appropriate measure/ quantity recommended for this meal (given the client/patient's specs). Meal for the given calorie intake should be measured in grams."
                    },
                    "alternative_measure": {
                        "type": "string",
                        "description": "Return a human equivalent measurement for the meal and given calories (given that gram might be hard to quantify for people without scales at home)."
                    }
                },  # end of dinner schedule
            }  # meal
        }
    }

function_instructions = [{
    "name": "generate_mealplan",
    "description": "Generate a 31-day Meal Plan: 1. **Daily Structure:** - **Breakfast:** Should include a good mix of carbohydrates and proteins to kickstart the day. - **Lunch:** A balanced meal with a focus on proteins, carbohydrates, and vegetables. - **Dinner:** A lighter meal that still provides necessary nutrients and proteins for muscle recovery.",
    "parameters": {
        "type": "object",
        "properties": meal_plan_format,
        "required": day_list
    }
}]


def createMealPlan(tribe, state, age, gender):
    prompt = f"""
     The patient profile is as follows:
    - **Tribe:** {tribe}
    - **State of Residence:** {state}
    - **Age:** {age}
    - **Gender:** {gender}
    - **Meal Goal:** Bodybuilding and maintaining overall health
    
    
    Requirements for Meal Plan:
    1. Daily Structure:
    - Breakfast: Should include a good mix of carbohydrates and proteins to kickstart the day.
    - Lunch: A balanced meal with a focus on proteins, carbohydrates, and vegetables.
    - Dinner: A lighter meal that still provides necessary nutrients and proteins for muscle recovery.
    
    2. Monthly Structure (for 31 days):
    - Create a varied meal plan for each week to avoid repetition and keep the diet interesting.
    
    3. Nutritional Balance:
    - Ensure each day's meals collectively meet the requirement.
    - Include a variety of protein sources to aid body building.
    - Incorporate healthy fats and avoid excessive use of oils or fried foods.
    - Ensure adequate fiber intake through vegetables and grains.
    
    4. Portion Sizes:
    - Specify portion sizes for each meal to align with the caloric intake.
    - Adjust portions as necessary to meet daily caloric goals.
     
    5. Cultural Appropriateness:
    - Use traditional Tribe Meals e.g …{tribe} meals that are common in Preferred Location eg. {state} and enjoyed by the patient.
    - Ensure meals are accessible and ingredients can be easily found in Preferred Location eg. {state}.
    
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are a professional dietitian tasked with creating a one-month meal plan for a specific patient based in Nigeria."},
            {"role": "user", "content": prompt}
        ],
        functions=function_instructions,
        function_call="auto"
    )

    result = response.choices[0].message

    if 'function_call' in result and 'arguments' in result['function_call']:
        return result['function_call']['arguments']
    else:
        return None
