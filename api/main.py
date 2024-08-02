from fastapi import FastAPI
from . import generate_mealplan as mp
import json

app = FastAPI()

@app.get("/get_mealplan/")
def getMealPlan(tribe: str, state: str, age: int, gender:str):
    try:
        results = mp.createMealPlan(tribe, state, age, gender)
        return json.dumps(results,default=str)
    except Exception as e:
        raise e
    return "Hello, World"

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app)
