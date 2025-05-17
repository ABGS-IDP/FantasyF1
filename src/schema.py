from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

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
    standings: List[str]


class Score(BaseModel):
    user_id: str
    race_id: str
    points: int


class UserStats(BaseModel):
    username: str
    drivers: List[str] = Field(default_factory=list)
    teams: List[str] = Field(default_factory=list)
    total_points: float
    total_budget: float
    bonuses: dict = Field(default_factory=dict)


class Bonus(str, Enum):
    twox = "2x"
    beat_teammate = "beat_teammate"
    both_drivers = "both_drivers"