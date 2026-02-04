from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Car(BaseModel):
    id: int
    name: str
    origin: str

cars: List[Car] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to Car House"}

@app.get("/cars") 
def get_cars():
    return cars

@app.post("/cars")
def add_car(car: Car):
    cars.append(car)
    return car

@app.put("/cars/{car_id}")
def update_car(car_id: int, updated_car: Car):
    for index, car in enumerate(cars):
        if car_id == car.id:
            cars[index] = updated_car
            return updated_car
    return {"error": "Car not found"}

@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    for index, car in enumerate(cars):
        if car.id == car_id:
            deleted_car = cars.pop(index)
            return deleted_car
    return {"erorr": "Car not found"}    
    
    