from pydantic import BaseModel, Field
from typing import Optional

class Driver(BaseModel):
    name: str
    team: str
    price: float
    championship_points: Optional[int] = Field(default=0)

class DriverUpdateRequest(BaseModel):
    team: Optional[str] = None
    price: Optional[float] = None
    championship_points: Optional[int] = Field(default=0)

class Team(BaseModel):
    name: str
    price: float

class Race(BaseModel):
    name: str
    date: str

class Score(BaseModel):
    user_id: str
    race_id: str
    points: int