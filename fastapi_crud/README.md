## Car House API
A simple FastAPI application for managing a car inventory with CRUD operations.

### Setup

    uv pip install fastapi uvicorn pydantic

### Run

    uvicorn main:app --reload
    Visit http://localhost:8000/docs for interactive API documentation.

### API Endpoints
    GET / - Welcome message
    GET /cars - Get all cars
    POST /cars - Add a car
    PUT /cars/{car_id} - Update a car
    DELETE /cars/{car_id} - Delete a car

### Example
    json
    {
        "id": 1,
        "name": "Tesla Model 3",
        "origin": "USA"
    }

Note: Uses in-memory storage. Data resets on restart.