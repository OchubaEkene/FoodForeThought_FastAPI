from fastapi import FastAPI
import generate_mealplan as mp
import json

app = FastAPI()

# # Mount the static directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/get_mealplan/")
def getMealPlan(tribe: str, state: str, age: int, gender:str):
    try:
        results = mp.createMealPlan(tribe, state, age, gender)
        return results
    except Exception as e:
        print(f"{e}")
        raise e
    

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app)
