from .schema import Bonus
from functools import reduce

placemnent_points = [ 25, 18, 15, 12, 10, 8, 6, 4, 2, 1 ]

def calculate_points_with_bonus(driver: dict, user: dict, points: int, drivers: list[dict]) -> None:
    """
    Calculate the points for a driver with bonus points.
    """

    points_from_drivers = points
    points_from_teams = reduce(lambda acc, x: acc + x[0], filter(lambda x: x[1]["team"] == driver["team"], zip(placemnent_points, drivers)), 0)

    bonuses = user["bonuses"]
    try:
        if Bonus.twox in bonuses[driver["name"]]:
            points_from_drivers = points_from_drivers * 2
            bonuses[driver["name"]].remove(Bonus.twox)
        if Bonus.twox in bonuses[driver["team"]]:
            points_from_teams = points_from_teams * 2
            bonuses[driver["team"]].remove(Bonus.twox)
    except Exception:
        pass
    try:
        if Bonus.beat_teammate in bonuses[driver["name"]]:
            points_from_drivers += 30 * (list(filter(lambda x: x["team"] == driver["team"], drivers))[0]['name'] == driver["name"])
            bonuses[driver["name"]].remove(Bonus.beat_teammate)
    except Exception:
        pass
    try:
        if Bonus.both_drivers in bonuses[driver["team"]]:
            points_from_teams += 60 * (len(list(filter(lambda x: x["team"] == driver["team"], drivers))) == 2)
            bonuses[driver["team"]].remove(Bonus.both_drivers)
    except Exception:
        pass

    if driver["name"] in user["drivers"]:
        user["total_points"] += points_from_drivers / 10
        user["total_budget"] += points_from_drivers / 10
    if driver["team"] in user["teams"]:
        user["total_points"] += points_from_teams / 20
        user["total_budget"] += points_from_teams / 20
