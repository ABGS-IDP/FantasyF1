from typing import List, Any
from fastapi import FastAPI, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .schema import Driver, Team, Race, UserStats, Bonus
from jose import jwt, JWTError
import httpx
from .utils import calculate_points_with_bonus, placemnent_points
import os


# TODO: move env variables to a config file
db_url = os.getenv("DBAPI_URL")
db_port = int(os.getenv("DBAPI_PORT", 8000))
AUTH_URL = os.getenv("AUTH_URL")

# FastAPI app
app = FastAPI(
    root_path="/api",
    openapi_tags=[
        {
            "name": "FantasyF1",
            "description": "Game logic for Fantasy Formula 1."
        }
    ]
)

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{AUTH_URL}/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload.get("sub"), "role": payload.get("role")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.get(
    "/drivers",
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
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error fetching available drivers: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get(
    "/teams",
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
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error fetching available teams: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get(
    "/bonuses",
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
                "description": "Double points for the driver or the team for one race."
            },
            {
                "name": "beat_teammate",
                "description": "+3 points if your driver beats their teammate."
            },
            {
                "name": "both_drivers",
                "description": "+3 points if both drivers finish in the top 10."
            }
        ]
    except HTTPException as e:
        raise e
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
    except HTTPException as e:
        raise e    
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post(
    "/teams",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def create_team(team: Team, current_user: dict = Depends(get_current_user)):
    """
    Create a new team.
    """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create teams")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{db_url}:{db_port}/teams/", json=team.model_dump())
            if response.status_code == 201:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except HTTPException as e:
        raise e    
    except Exception as e:
        print(f"Error creating team: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.delete(
    "/teams/{team_id}",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def delete_team(team_id: str, current_user: dict = Depends(get_current_user)):
    """
    Delete a team.
    """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete teams")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{db_url}:{db_port}/teams/{team_id}")
            if response.status_code == 204:
                return {"message": "Team deleted successfully."}
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error deleting team: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post(
    "/drivers",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def create_driver(driver: Driver, current_user: dict = Depends(get_current_user)):
    """
    Create a new driver.
    """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create drivers")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{db_url}:{db_port}/drivers/", json=driver.model_dump())
            if response.status_code == 201:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error creating driver: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.delete(
    "/driver/{drivername}",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def delete_driver(drivername: str, current_user: dict = Depends(get_current_user)):
    """
    Delete a driver.
    """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete drivers")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{db_url}:{db_port}/drivers/{drivername}")
            if response.status_code == 204:
                return {"message": "Driver deleted successfully."}
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error deleting driver: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post(
    "/races",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def create_race(race: Race, current_user: dict = Depends(get_current_user)):
    """
    Create race
    """

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create races")
    try:
        async with httpx.AsyncClient() as client:
            
            drivers = (await client.get(f"{db_url}:{db_port}/drivers/")).json()
            assert all(map(lambda x: x["name"] in race.standings, drivers)), "All drivers must be in the standings"

            response = await client.post(f"{db_url}:{db_port}/races/", json=race.model_dump())
            if response.status_code == 201:

                users = (await client.get(f"{db_url}:{db_port}/users/")).json()
                

                driver_objects = [next((d for d in drivers if d["name"] == driver_name), None) for driver_name in race.standings]

                for driver_name, points_gained in zip(race.standings, placemnent_points):
                    driver = next((d for d in drivers if d["name"] == driver_name), None)
                    if driver:
                        driver["championship_points"] += points_gained
                        await client.put(f"{db_url}:{db_port}/drivers/{driver_name}", json=driver)

                        for user in users:
                            calculate_points_with_bonus(driver, user, points_gained, driver_objects)
                            await client.put(f"{db_url}:{db_port}/users/{user['username']}", json=user)

                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
            
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error creating race: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.delete(
    "/race/{race_id}",
    response_model=Any,
    tags=["Admin Endpoints"]
)
async def delete_race(race_id: str, current_user: dict = Depends(get_current_user)):
    """
    Delete a race.
    """

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete races")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{db_url}:{db_port}/races/{race_id}")
            if response.status_code == 204:
                return {"message": "Race deleted successfully."}
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error deleting race: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/buy_driver",
    response_model=Any,
    tags=["FantasyF1"]
)
async def buy_driver(drivername: str, current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    async with httpx.AsyncClient() as client:
        user = (await client.get(f"{db_url}:{db_port}/users/{username}")).json()
        driver = (await client.get(f"{db_url}:{db_port}/drivers/{drivername}")).json()

        if drivername in user["drivers"]:
            raise HTTPException(status_code=400, detail="Driver already in roster")

        if len(user["drivers"]) >= 2:
            raise HTTPException(status_code=400, detail="Maximum 2 drivers allowed")

        if user["total_budget"] < driver["price"]:
            raise HTTPException(status_code=400, detail="Insufficient budget")

        user["drivers"].append(drivername)
        user["total_budget"] -= driver["price"]

        await client.put(f"{db_url}:{db_port}/users/{username}", json=user)
        return UserStats(**user)


@app.post(
    "/buy_team",
    response_model=Any,
    tags=["FantasyF1"]
)
async def buy_team(teamname: str, current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    async with httpx.AsyncClient() as client:
        user = (await client.get(f"{db_url}:{db_port}/users/{username}")).json()
        teams = (await client.get(f"{db_url}:{db_port}/teams/")).json()
        team_data = next((t for t in teams if t["name"] == teamname), None)

        if not team_data:
            raise HTTPException(status_code=404, detail="Team not found")

        if teamname in user["teams"]:
            raise HTTPException(status_code=400, detail="Team already in roster")

        if len(user["teams"]) >= 2:
            raise HTTPException(status_code=400, detail="Maximum 2 teams allowed")

        if user["total_budget"] < team_data["price"]:
            raise HTTPException(status_code=400, detail="Insufficient budget")

        user["teams"].append(teamname)
        user["total_budget"] -= team_data["price"]

        await client.put(f"{db_url}:{db_port}/users/{username}", json=user)
        return UserStats(**user)


@app.get(
    "/{username}/drivers",
    response_model=Any,
    tags=["FantasyF1"]
)
async def get_drivers(username: str):
    async with httpx.AsyncClient() as client:
        user = (await client.get(f"{db_url}:{db_port}/users/{username}")).json()
        return user["drivers"]


@app.get(
    "/{username}/teams",
    response_model=Any,
    tags=["FantasyF1"]
)
async def get_teams(username: str):
    async with httpx.AsyncClient() as client:
        user = (await client.get(f"{db_url}:{db_port}/users/{username}")).json()
        return user["teams"]


@app.put(
    "/change_driver",
    response_model=UserStats,
    tags=["FantasyF1"]
)
async def change_driver(current_driver: str, new_driver: str, current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    async with httpx.AsyncClient() as client:
        user = (await client.get(f"{db_url}:{db_port}/users/{username}")).json()

        if current_driver not in user["drivers"]:
            raise HTTPException(status_code=404, detail="Current driver not in roster")

        new_driver_data = (await client.get(f"{db_url}:{db_port}/drivers/{new_driver}")).json()

        if user["total_budget"] < new_driver_data["price"]:
            raise HTTPException(status_code=400, detail="Insufficient budget")

        user["drivers"].remove(current_driver)
        user["drivers"].append(new_driver)
        user["total_budget"] -= new_driver_data["price"]

        await client.put(f"{db_url}:{db_port}/users/{username}", json=user)
        return UserStats(**user)


@app.put(
    "/change_team",
    response_model=Any,
    tags=["FantasyF1"]
)
async def change_team(current_team: str, new_team: str, current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    async with httpx.AsyncClient() as client:
        user = (await client.get(f"{db_url}:{db_port}/users/{username}")).json()
        teams = (await client.get(f"{db_url}:{db_port}/teams/")).json()
        new_team_data = next((t for t in teams if t["name"] == new_team), None)

        if current_team not in user["teams"]:
            raise HTTPException(status_code=404, detail="Current team not in roster")

        if not new_team_data:
            raise HTTPException(status_code=404, detail="New team not found")

        if user["total_budget"] < new_team_data["price"]:
            raise HTTPException(status_code=400, detail="Insufficient budget")

        user["teams"].remove(current_team)
        user["teams"].append(new_team)
        user["total_budget"] -= new_team_data["price"]

        await client.put(f"{db_url}:{db_port}/users/{username}", json=user)
        return UserStats(**user)


@app.get(
    "/{username}/points",
    response_model=Any,
    tags=["FantasyF1"]
)
async def get_points(username: str):
    async with httpx.AsyncClient() as client:
        user = (await client.get(f"{db_url}:{db_port}/users/{username}")).json()
        return user["total_points"]


@app.get(
    "/budget",
    response_model=Any,
    tags=["FantasyF1"]
)
async def get_budget(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    async with httpx.AsyncClient() as client:
        user = (await client.get(f"{db_url}:{db_port}/users/{username}")).json()
        return user["total_budget"]


@app.post(
    "/buy_bonus",
    response_model=Any,
    tags=["FantasyF1"]
)
async def buy_bonus(target_name: str, bonus_type: Bonus, current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    VALID_BONUSES = {"2x", "beat_teammate", "both_drivers"}

    if bonus_type not in VALID_BONUSES:
        raise HTTPException(status_code=400, detail="Invalid bonus type")

    async with httpx.AsyncClient() as client:
        user = (await client.get(f"{db_url}:{db_port}/users/{username}")).json()

        if user["total_budget"] < 1.0:
            raise HTTPException(status_code=400, detail="Insufficient budget for bonus")

        if target_name not in user["drivers"] and target_name not in user["teams"]:
            raise HTTPException(status_code=404, detail="Target not in user roster")

        if "bonuses" not in user or not isinstance(user["bonuses"], dict):
            user["bonuses"] = {}

        if target_name not in user["bonuses"]:
            user["bonuses"][target_name] = []

        user["bonuses"][target_name].append(bonus_type)
        user["total_budget"] -= 1.0

        await client.put(f"{db_url}:{db_port}/users/{username}", json=user)
        return UserStats(**user)
