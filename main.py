from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define the Pydantic model for city
class City(BaseModel):
    city: str
    timezone: str 

# In-memory database (list of cities)
db: List[City] = []

@app.get("/")
def index():
    return {'Hello': 'world'}

@app.get("/cities")
def get_cities():
    return db

@app.get("/cities/{city_id}")
def get_city(city_id: int):
    return db[city_id]

@app.post("/cities")
def create_city(city: City):
    db.append(city.dict())  # Append the city as a dictionary to the database
    return db[-1]

@app.delete("/cities/{city_id}")
def delete_city(city_id: int):
    deleted_city = db.pop(city_id)  # Remove and return the city
    return {"message": "City deleted", "city": deleted_city}
        
