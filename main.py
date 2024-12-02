from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

import requests


app = FastAPI()

# Define the Pydantic model for city
class City(BaseModel):
    city: str
    timezone: str 

# In-memory database (list of cities)
db: List[City] = []

@app.get("/hello/{'world'}")
def index1(world):
    return {'hello' : 'world'}

@app.get("/cities")
def get_cities2():
    results = []
    headers = {
        "X-Api-Key": "your-API-key"  # Replace with your actual API key
    }
    for city in db:
        r = requests.get(f'https://api.api-ninjas.com/v1/worldtime?timezone={city["timezone"]}', headers=headers)
        if r.status_code == 200:
            current_time = r.json().get('datetime', 'Unknown time')
            results.append({'name': city['city'], 'timezone': city['timezone'], 'current_time': current_time})
    return results


@app.get("/cities/{city_id}")
def get_city3(city_id: int):
    return db[city_id-1]

@app.post("/cities")
def create_city(city: City):
    db.append(city.dict())  # Append the city as a dictionary to the database
    return db[-1]

@app.delete("/cities/{city_id}")
def delete_city(city_id: int):
    deleted_city = db.pop(city_id)  # Remove and return the city
    return {"message": "City deleted", "city": deleted_city}
        






