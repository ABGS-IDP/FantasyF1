from typing import List, Any
from fastapi import FastAPI, HTTPException
from .models import Driver, Team
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
    response_model=Any,
    tags=["FantasyF1"]
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
    response_model=Any,
    tags=["FantasyF1"]
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
    

@app.get(
    "/availableDrivers",
    response_model=Any,
    tags=["FantasyF1"]
)
async def get_available_drivers() -> List[dict]:
    """
    Get all available drivers.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{db_url}:{db_port}/drivers/")
            return response.json()
    except Exception as e:
        print(f"Error fetching available drivers: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get(
    "/availableTeams",
    response_model=Any,
    tags=["FantasyF1"]
)
async def get_available_teams() -> List[dict]: 
    """
    Get all available teams.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{db_url}:{db_port}/teams/")
            return response.json()
    except Exception as e:
        print(f"Error fetching available teams: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get(
    "/availableBonuses",
    response_model=Any,
    tags=["FantasyF1"]
)
async def get_available_bonuses() -> List[dict]:
    """
    Get all available bonuses.
    """
    try:
        return [
            {
                "name": "2x",
                "description": "Double points for the driver for one race."
            },
            {
                "name": "Teammate wins",
                "description": "+10 points if your driver wins and their teammate finishes in the top 5."
            },
            {
                "name": "Extra points",
                "description": "+25 points if your driver takes pole position."
            }
        ]
    except Exception as e:
        print(f"Error fetching available bonuses: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get(
    "/leaderboard",
    response_model=Any,
    tags=["FantasyF1"]
)
async def get_leaderboard() -> List[dict]:
    """
    Get the leaderboard.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{db_url}:{db_port}/users/")
            leaderboard: List = response.json()
            leaderboard.sort(key=lambda x: x["total_points"], reverse=True)
            return leaderboard
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post(
    "/createTeam",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def create_team(team: Team):
    """
    Create a new team.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{db_url}:{db_port}/teams/", json=team.model_dump())
            if response.status_code == 201:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except Exception as e:
        print(f"Error creating team: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.delete(
    "/deleteTeam/{team_id}",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def delete_team(team_id: str):
    """
    Delete a team.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{db_url}:{db_port}/teams/{team_id}")
            if response.status_code == 204:
                return {"message": "Team deleted successfully."}
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except Exception as e:
        print(f"Error deleting team: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post(
    "/createDriver",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def create_driver(driver: Driver):
    """
    Create a new driver.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{db_url}:{db_port}/drivers/", json=driver.model_dump())
            if response.status_code == 201:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except Exception as e:
        print(f"Error creating driver: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.delete(
    "/deleteDriver/{driver_id}",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def delete_driver(driver_id: str):
    """
    Delete a driver.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{db_url}:{db_port}/drivers/{driver_id}")
            if response.status_code == 204:
                return {"message": "Driver deleted successfully."}
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except Exception as e:
        print(f"Error deleting driver: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post(
    "/createRace",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def create():
    """
    Create
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{db_url}:{db_port}/races/")
            if response.status_code == 201:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except Exception as e:
        print(f"Error creating race: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.delete(
    "/deleteRace/{race_id}",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def delete_driver(race_id: str):
    """
    Delete a driver.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{db_url}:{db_port}/races/{race_id}")
            if response.status_code == 204:
                return {"message": "Race deleted successfully."}
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except Exception as e:
        print(f"Error deleting race: {e}")
        raise HTTPException(status_code=500, detail=str(e))