from openai import OpenAI
import json

with open('config.json', 'r') as keys:
    secret_keys = json.load(keys)

client = OpenAI(
  organization=secret_keys["openai_api_org"],
  project=secret_keys["openai_project_id"],
  api_key=secret_keys["openai_api_key"]
)

def generate_mealplan():
    pass

meal_plan_format = {}
day_list = []

for day in range(0, 31):
    day_list.append(f'day_{day + 1}')
    meal_plan_format[f'day_{day + 1}'] = {
        "type": "object",
        "description": f"meal plan for day {day + 1}'s meal breakdown for breakfast, lunch, and dinner.",
        "properties": {
            "breakfast": {
                "type": "object",
                "properties": {
                    "meal_name": {
                        "type": "string"
                    },
                    "food_category": {
                        "type": "string"
                    },
                    "calories_meal_intake": {
                        "type": "number"
                    },
                    "meal_measure_gram": {
                        "type": "number"
                    },
                    "human_equivalent_alternative_measure": {
                        "type": "string"
                    }
                },  # end of breakfast schedule
            },  # meal
            "lunch": {
                "type": "object",
                "properties": {
                    "meal_name": {
                        "type": "string"
                    },
                    "food_category": {
                        "type": "string"
                    },
                    "calories_meal_intake": {
                        "type": "number"
                    },
                    "meal_measure_gram": {
                        "type": "number"
                    },
                    "human_equivalent_alternative_measure": {
                        "type": "string"
                    }
                },  # end of lunch schedule
            },  # meal
            "dinner": {
                "type": "object",
                "properties": {
                    "meal_name": {
                        "type": "string"
                    },
                    "food_category": {
                        "type": "string"
                    },
                    "calories_meal_intake": {
                        "type": "number"
                    },
                    "meal_measure_gram": {
                        "type": "number"
                    },
                    "human_equivalent_alternative_measure": {
                        "type": "string"
                    }
                },  # end of dinner schedule
            }  # meal
        }
    }

function_instructions = [{
    "name": "generate_mealplan",
    "description": "Generate a 31-day Meal Plan (Breakfast, Lunch and Dinner.",
    "parameters": {
        "type": "object",
        "properties": meal_plan_format,
        "required": day_list
    }
}]


def createMealPlan(tribe, state, age, gender):
    prompt = f"""
     The patient profile is as follows:
    - Tribe: {tribe}
    - State of Residence: {state}
    - Age: {age}
    - Gender: {gender}
    - Meal Goal: Bodybuilding and maintaining overall health
    
    
    Requirements for Meal Plan:
    1. Daily Structure:
    - Breakfast: Should include a good mix of carbohydrates and proteins to kickstart the day.
    - Lunch: A balanced meal with a focus on proteins, carbohydrates, and vegetables.
    - Dinner: A lighter meal that still provides necessary nutrients and proteins for muscle recovery.
    
    2. Monthly Structure (for 31 days):
    - Create a varied meal plan for each week to avoid repetition and keep the diet interesting.
    
    3.Cultural Appropriateness:
    - Use traditional Tribe Meals e.g …{tribe} meals that are common in Preferred Location eg. {state} and enjoyed by the patient.
    - Ensure meals are accessible and ingredients can be easily found in Preferred Location eg. {state}.
    
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        # response_format={ "type": "json_object" },
        seed=4,
        temperature=0,
        messages=[
            {"role": "system",
             "content": "You are a professional dietitian tasked with creating a one-month meal plan for a specific patient based in Nigeria."},
            {"role": "user", "content": prompt}
        ],
        functions=function_instructions,
        function_call="auto")

    result = response.choices[0].message
        
    if result.function_call.arguments:
        return json.loads(result.function_call.arguments)
    else:
        return None
