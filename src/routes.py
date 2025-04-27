from typing import List, Any
from fastapi import FastAPI, HTTPException
import httpx

# TODO: move env variables to a config file
db_url = "http://localhost"
db_port = 8000

# FastAPI app
app = FastAPI(
    openapi_tags=[
        {
            "name": "FantasyF1",
            "description": "All Fantasy Formula 1 API endpoints."
        }
    ]
)

@app.get(
    "/drivers",
    response_model=Any
)
async def get_drivers() -> List[dict]:
    """
    Get all drivers.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{db_url}:{db_port}/drivers/")
            return response.json()
    except Exception as e:
        print(f"Error fetching drivers: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post(
    "/register",
    response_model=Any
)
async def register_user(user: dict) -> dict:
    """
    Register a new user.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{db_url}:{db_port}/register/", json=user)
            if response.status_code == 201:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except Exception as e:
        print(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail=str(e))
