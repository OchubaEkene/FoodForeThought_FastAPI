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


days=14
function_instructions = [
{
  "name": "generate_mealplan",
  "description": f"Generate a {days}-day Meal Plan with Breakfast, Lunch, and Dinner for each day.",
  "parameters": {
    "type": "object",
    "properties": {
      "meal_plan": {
        "type": "object",
        "description": f"Dictionary of meal plans for {days} days, each day contains arrays for breakfast, lunch, and dinner.",
        "properties": {
          "days": {
            "type": "array",
            "description": "List of days in the meal plan.",
            "items": {
              "type": "integer",
              "description": f"Day number (1 to {days})."
            },
            "minItems": days,
            "maxItems": days
          },
          "meals": {
            "type": "array",
            "description": f"List of meal arrays for each of the {days} days.",
            "items": {
              "type": "array",
              "description": "Array containing breakfast, lunch, and dinner for each day.",
              "items": {
                "type": "object",
                "properties": {
                  "meal_name": {
                    "type": "string",
                    "description": "Name of the meal"
                  },
                  "food_category": {
                    "type": "string",
                    "description": "Category of the meal"
                  },
                  "calories_meal_intake": {
                    "type": "number",
                    "description": "Calories intake for the meal"
                  },
                  "meal_measure_gram": {
                    "type": "number",
                    "description": "Measurement in grams for the meal"
                  },
                  "human_equivalent_alternative_measure": {
                    "type": "string",
                    "description": "Human equivalent alternative measurement for the meal"
                  }
                },
                "required": ["meal_name", "food_category", "calories_meal_intake", "meal_measure_gram", "human_equivalent_alternative_measure"]
              },
              "minItems": 3,
              "maxItems": 3
            },
            "minItems": days,
            "maxItems": days
          }
        },
        "required": ["days", "meals"]
      }
    },
    "required": ["meal_plan"]
  }
}
]


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
    
    2. Monthly Structure (for {days} days):
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
             "content": "You are a professional dietitian tasked with creating a {days} days meal plan for a specific patient based in Nigeria."},
            {"role": "user", "content": prompt}
        ],
        functions=function_instructions,
        function_call="auto")

    result = response.choices[0].message
    
    
    if result.function_call.arguments:
        return json.loads(result.function_call.arguments)
    else:
        return {}
